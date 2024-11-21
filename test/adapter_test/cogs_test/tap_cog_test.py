import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from adapter.cogs.tap_cog import TapCommand
from domain.entities.roll_result import AdvantageType
from discord import app_commands

class TestTapCommand(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = MagicMock()  # Simula el bot de Discord
        self.cog = TapCommand(self.bot)  # Instancia la clase con el bot simulado
        self.command = self.cog.tap  # Referencia al comando tap

    @patch('adapter.presenters.roll_presenter.RollPresenter.roll')
    @patch('domain.interactors.roll_interactor.roll')
    async def test_roll_command(self, mock_roll, mock_roll_presenter):
        # Configurar mocks
        mock_roll_result = MagicMock(total=18, expr="1d20+2")
        mock_roll.return_value = mock_roll_result  # Simular el resultado de la tirada
        mock_interaction = AsyncMock()  # Simular la interacción de Discord

        # Acceder al callback del comando 'roll'
        command = self.cog.roll

        # Ejecutar el callback del comando con los argumentos simulados
        await command.callback(
            self.cog,  # Pasar el contexto de la cog
            mock_interaction,  # Simular la interacción
            "1d20+2"  # Argumento del comando
        )

        # Verificar que se llamó a roll_interactor.roll con los argumentos esperados
        mock_roll.assert_called_once_with("1d20+2")

        # Verificar que se llamó a RollPresenter.roll con el resultado de la tirada
        mock_roll_presenter.assert_called_once_with(mock_roll_result)

    @patch('domain.interactors.roll_interactor.skill_test')
    @patch('adapter.config.repository.get')
    @patch('adapter.presenters.roll_presenter.RollPresenter.skill_test')
    async def test_tap_command_with_active_character(
        self, mock_roll_presenter, mock_repository_get, mock_skill_test
    ):
        # Configurar mocks
        mock_character = MagicMock()
        mock_character.skills.__dict__ = {"athletics": MagicMock(modifier=3)}
        mock_repository_get.return_value = mock_character

        # Simular el resultado de skill_test
        mock_roll_result = MagicMock(total=18, expr="2d20kh1+3")
        mock_skill_test_result = MagicMock(roll_result=mock_roll_result, plot_die_result=None)
        mock_skill_test.return_value = mock_skill_test_result

        mock_interaction = AsyncMock()  # Simular la interacción de Discord

        # Crear una simulación de los argumentos del comando
        stat_choice = app_commands.Choice(name="Athletics", value="athletics")
        advantage = AdvantageType.ADVANTAGE.value
        plot_die = True
        plot_advantage = AdvantageType.DISADVANTAGE.value

        # Simular la invocación del comando
        await self.cog.tap.callback(
            self.cog,  # Pasar el contexto de la cog
            mock_interaction,  # Interacción simulada
            stat=stat_choice,
            advantage=advantage,
            plot_die=plot_die,
            plot_advantage=plot_advantage
        )

        # Verificar que se accedió al repositorio
        mock_repository_get.assert_called_once_with(
            str(mock_interaction.user.id), str(mock_interaction.guild.id)
        )

        # Verificar que se llamó a skill_test con los argumentos esperados
        mock_skill_test.assert_called_once_with(
            modifier=3,
            advantage=AdvantageType.ADVANTAGE,
            plot_die=True,
            plot_advantage=AdvantageType.DISADVANTAGE
        )

        # Verificar que se llamó a RollPresenter con los argumentos esperados
        mock_roll_presenter.assert_called_once_with(
            mock_skill_test_result,
            skill="Athletics"
        )

    @patch('adapter.config.repository.get')
    async def test_tap_command_no_active_character(self, mock_repository_get):
        # Configurar mocks
        mock_repository_get.return_value = None  # Simular que no hay personaje activo
        mock_interaction = AsyncMock()

        # Ejecutar el comando
        await self.cog.tap.callback(
            self.cog,
            mock_interaction,
            stat=app_commands.Choice(name="Athletics", value="athletics"),
            advantage=AdvantageType.NONE.value,
            plot_die=False,
            plot_advantage=AdvantageType.NONE.value
        )

        # Verificar que se envió el mensaje de error
        mock_interaction.followup.send.assert_called_once_with(
            'Unexpected error occurred.', 
            ephemeral=True
        )
