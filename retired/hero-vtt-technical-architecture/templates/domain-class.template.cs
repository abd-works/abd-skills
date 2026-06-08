// ──────────────────────────────────────────────────────────────────────────────
// Template: {Domain}.cs — Domain class
// Reference: inputs/architecture-reference.md §Architecture Layers (Domain)
//            + §Mechanism: COH Game Bridge Seam
//            + §Mechanism: Direct Memory Manipulation
//
// Replace:
//   {Domain}        — domain class name, e.g. Identity, Movement, Crowd
//   {IDomain}       — domain interface, e.g. IIdentity
//   {SelectedType}  — child type managed by this domain class
//
// Rules enforced (see rules/):
//   ✔ Constructor receives IGameCommandExecutor and/or IMemoryInstance — never concrete types.
//   ✔ No MemorySharp import. No HookCostume reference. No address offsets.
//   ✔ INotifyPropertyChanged raised on state-changing properties.
//   ✔ Cross-feature consistency via domain-to-domain subscription — no ViewModel coordination.
// ──────────────────────────────────────────────────────────────────────────────

using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using Library.GameCommunicator;     // IGameCommandExecutor
using Library.ProcessCommunicator;  // IMemoryInstance

namespace Module.HeroVirtualTabletop.{Feature}
{
    public class {Domain} : I{Domain}, INotifyPropertyChanged
    {
        private readonly IGameCommandExecutor _executor;
        private readonly IMemoryInstance _memory;

        // ── Constructor ──────────────────────────────────────────────────────
        public {Domain}(IGameCommandExecutor executor, IMemoryInstance memory)
        {
            _executor = executor;
            _memory   = memory;
            Items     = new ObservableCollection<{SelectedType}>();
        }

        // ── State ─────────────────────────────────────────────────────────────
        public ObservableCollection<{SelectedType}> Items { get; }

        private bool _isActive;
        public bool IsActive
        {
            get => _isActive;
            private set { _isActive = value; OnPropertyChanged(); }
        }

        // ── Domain methods ────────────────────────────────────────────────────
        // Replace with real business operations from the story acceptance criteria.

        public void {DomainAction1}({SelectedType} item)
        {
            // Business rule: validate, mutate state, call game seam if needed.
            // Example: build keybind, call _executor.ExecuteCmd(keybind).
            // Example: call _memory.SetPosition(x, y, z).
            // Raise PropertyChanged / CollectionChanged when done.
        }

        // public void {DomainAction2}({SelectedType} item) { ... }

        // ── INotifyPropertyChanged ─────────────────────────────────────────────
        public event PropertyChangedEventHandler? PropertyChanged;
        private void OnPropertyChanged([CallerMemberName] string? name = null) =>
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }
}
