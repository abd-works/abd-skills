// ──────────────────────────────────────────────────────────────────────────────
// Template: Test{Feature}Domain.cs — Tier 1: Domain test
// Reference: inputs/architecture-reference.md §Testing Architecture (Tier 1)
//
// Replace:
//   {Feature}       — feature name, e.g. Identity, Movement
//   {Domain}        — domain class, e.g. Identity
//   {SelectedType}  — child type, e.g. IIdentity
//
// Rules enforced (see rules/):
//   ✔ No WPF imports (no BindableBase, DelegateCommand, ObservableCollection from Prism UI).
//   ✔ COH seam stubbed: FakeMemoryInstance + NoOpGameCommandExecutor.
//   ✔ One [TestClass] per story; one [TestMethod] per scenario (Given/When/Then naming).
//   ✔ Assert domain post-state, not ViewModel state.
// ──────────────────────────────────────────────────────────────────────────────

using FluentAssertions;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Library.GameCommunicator;    // NoOpGameCommandExecutor
using Library.ProcessCommunicator; // FakeMemoryInstance
using Module.HeroVirtualTabletop.{Feature};

namespace Module.UnitTest.Domain
{
    [TestClass]
    public class Test{Feature}Domain
    {
        private FakeMemoryInstance _memory = null!;
        private NoOpGameCommandExecutor _executor = null!;
        private {Domain} _{domainField} = null!;

        [TestInitialize]
        public void Given{Setup}()
        {
            _memory   = new FakeMemoryInstance();
            _executor = new NoOpGameCommandExecutor();
            _{domainField} = new {Domain}(_executor, _memory);

            // Pre-seed memory state if the test needs it:
            // _memory.SetXYZ(100f, 0f, 200f);
            // _memory.SetLabel("Hero1");
        }

        // ── Scenario: one [TestMethod] per acceptance criterion ───────────────

        [TestMethod]
        public void When{Action}_Then{ExpectedOutcome}()
        {
            // Arrange: any additional pre-state beyond [TestInitialize]

            // Act
            _{domainField}.{DomainAction}(/* args */);

            // Assert domain post-state
            _{domainField}.IsActive.Should().BeTrue();

            // Assert game seam was called correctly (Path 1)
            _executor.LastCommand.Should().Contain("expected_keybind_fragment");

            // Assert memory was written correctly (Path 2)
            _memory.ReadXYZ().Should().Be((100f, 0f, 200f));
        }

        // Add one [TestMethod] per story scenario.
    }
}
