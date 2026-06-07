using FluentAssertions;
using Library.GameCommunicator;
using Library.ProcessCommunicator;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Module.HeroVirtualTabletop.Characters;

namespace Module.UnitTest.Presentation
{
    [TestClass]
    public class TestCharacterViewModel
    {
        private FakeMemoryInstance _memory = null!;
        private Character _character = null!;
        private CharacterViewModel _vm = null!;

        [TestInitialize]
        public void GivenAViewModelWiredToARealCharacter()
        {
            _memory = new FakeMemoryInstance();
            _character = new Character(new NoOpGameCommandExecutor(), _memory)
                { Name = "Hero1" };
            _memory.SetLabel("Hero1");
            _vm = new CharacterViewModel(_character);
        }

        [TestMethod]
        public void WhenSpawnCommandExecuted_ThenBindingAndDomainBothUpdate()
        {
            _vm.SpawnCommand.Execute();

            _vm.IsSpawned.Should().BeTrue();
            _character.IsSpawned.Should().BeTrue();
        }
    }
}
