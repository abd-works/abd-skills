// ──────────────────────────────────────────────────────────────────────────────
// Template: Test{Feature}ViewModel.cs — Tier 2: ViewModel + Domain test
// Reference: inputs/architecture-reference.md §Testing Architecture (Tier 2)
//
// Replace:
//   {Feature}       — feature name, e.g. IdentityEditor
//   {Domain}        — domain class, e.g. Identity
//   {SelectedType}  — child type, e.g. IIdentity
//
// Rules enforced (see rules/):
//   ✔ Real domain class wired to the ViewModel — not a mock of the domain.
//   ✔ COH seam stubbed: FakeMemoryInstance + NoOpGameCommandExecutor.
//   ✔ Asserts BOTH binding state (ViewModel property) AND domain post-state.
//   ✔ One [TestClass] per story; one [TestMethod] per scenario.
// ──────────────────────────────────────────────────────────────────────────────

using FluentAssertions;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Library.GameCommunicator;    // NoOpGameCommandExecutor
using Library.ProcessCommunicator; // FakeMemoryInstance
using Module.HeroVirtualTabletop.{Feature};

namespace Module.UnitTest.Presentation
{
    [TestClass]
    public class Test{Feature}ViewModel
    {
        private FakeMemoryInstance _memory = null!;
        private {Domain} _{domainField} = null!;
        private {Feature}ViewModel _vm = null!;

        [TestInitialize]
        public void Given{Setup}()
        {
            _memory      = new FakeMemoryInstance();
            _{domainField} = new {Domain}(new NoOpGameCommandExecutor(), _memory);
            _vm          = new {Feature}ViewModel(_{domainField});

            // Wire SelectedItem if the command requires a selection:
            // _vm.SelectedItem = _{domainField}.Items.First();
        }

        // ── Scenario: assert binding AND domain post-state ────────────────────

        [TestMethod]
        public void When{UserGesture}_Then{BindingUpdatesAndDomainStateCorrect}()
        {
            // Arrange
            var item = /* create or pick an item */;
            _vm.SelectedItem = item;

            // Act: execute the ViewModel command (simulates user gesture)
            _vm.{Command1}.Execute();

            // Assert binding state (ViewModel layer)
            _vm.SelectedItem.Should().Be(item);

            // Assert domain post-state (domain layer)
            item.IsActive.Should().BeTrue();
        }

        // Add one [TestMethod] per story scenario.
    }
}
