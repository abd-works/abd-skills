using FluentAssertions;
using Library.GameCommunicator;
using Library.ProcessCommunicator;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Module.HeroVirtualTabletop.Characters;

namespace Module.UnitTest.Domain
{
    [TestClass]
    public class TestCharacterDomain
    {
        private FakeMemoryInstance _memory = null!;
        private NoOpGameCommandExecutor _executor = null!;
        private Character _character = null!;

        [TestInitialize]
        public void GivenACharacter()
        {
            _memory = new FakeMemoryInstance();
            _executor = new NoOpGameCommandExecutor();
            _character = new Character(_executor, _memory) { Name = "Hero1" };
            _memory.SetLabel("Hero1");
        }

        [TestMethod]
        public void WhenSpawned_ThenIsSpawnedAndCommandSent()
        {
            _character.Spawn();

            _character.IsSpawned.Should().BeTrue();
            _executor.LastCommand.Should().Contain("Hero1");
        }

        [TestMethod]
        public void WhenTurned_ThenPositionRestored()
        {
            _memory.SetXYZ(10f, 0f, 20f);

            _character.TurnTo(90f);

            _memory.ReadXYZ().Should().Be((10f, 0f, 20f));
        }
    }
}
