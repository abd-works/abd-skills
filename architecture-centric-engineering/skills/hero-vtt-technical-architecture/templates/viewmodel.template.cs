// ──────────────────────────────────────────────────────────────────────────────
// Template: {Feature}ViewModel.cs — Skinny ViewModel
// Reference: inputs/architecture-reference.md §Mechanism: Skinny ViewModel
//
// Replace:
//   {Feature}       — feature name, e.g. IdentityEditor
//   {Domain}        — domain class name, e.g. Identity
//   {IDomain}       — domain interface, e.g. IIdentity  (or Character, etc.)
//   {SelectedType}  — type of selected item, e.g. IIdentity
//   {CommandN}      — DelegateCommand name per user story action
//   {DomainMethod}  — the one domain method the command delegates to
//
// Rules enforced (see rules/):
//   ✔ Every command handler is a one-liner: delegate to domain, done.
//   ✔ No game internals (no reference to IGameCommandExecutor, IMemoryInstance, or concrete COH types).
//   ✔ Observable properties are direct domain references — no copy, no local sync.
// ──────────────────────────────────────────────────────────────────────────────

using System.Collections.ObjectModel;
using Prism.Commands;
using Prism.Mvvm;
using Module.HeroVirtualTabletop.{Feature};

namespace Module.HeroVirtualTabletop.{Feature}
{
    public class {Feature}ViewModel : BindableBase
    {
        private readonly {IDomain} _{domainField};

        // ── Constructor ──────────────────────────────────────────────────────
        public {Feature}ViewModel({IDomain} {domainField})
        {
            _{domainField} = {domainField};

            // Wire commands — one DelegateCommand per user story action.
            {Command1} = new DelegateCommand({Command1Handler}, Can{Command1})
                .ObservesProperty(() => SelectedItem);

            // Add additional DelegateCommands here, one per action.
        }

        // ── Bound properties ─────────────────────────────────────────────────
        // Direct reference to domain collection — no copy, no sync.
        public ObservableCollection<{SelectedType}> Items => _{domainField}.Items;

        private {SelectedType}? _selectedItem;
        public {SelectedType}? SelectedItem
        {
            get => _selectedItem;
            set => SetProperty(ref _selectedItem, value);
        }

        // ── Commands ─────────────────────────────────────────────────────────
        public DelegateCommand {Command1} { get; }

        // One-liner: call the domain method, done.
        private void {Command1Handler}() =>
            _{domainField}.{DomainMethod1}(SelectedItem!);

        private bool Can{Command1}() => SelectedItem != null;

        // ── Additional commands follow the same pattern ───────────────────────
        // public DelegateCommand {Command2} { get; }
        // private void {Command2Handler}() => _{domainField}.{DomainMethod2}(SelectedItem!);
        // private bool Can{Command2}() => SelectedItem != null;
    }
}
