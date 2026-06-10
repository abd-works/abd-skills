using System.ComponentModel;
using System.Runtime.CompilerServices;
using Library.GameCommunicator;
using Library.ProcessCommunicator;

namespace Module.HeroVirtualTabletop.Characters
{
    public class Character : INotifyPropertyChanged
    {
        private readonly IGameCommandExecutor _executor;
        private readonly IMemoryInstance _memory;

        public Character(IGameCommandExecutor executor, IMemoryInstance memory)
        {
            _executor = executor;
            _memory = memory;
        }

        public string Name { get; set; } = string.Empty;

        private bool _isSpawned;
        public bool IsSpawned
        {
            get => _isSpawned;
            private set { _isSpawned = value; OnPropertyChanged(); }
        }

        public void Spawn()
        {
            _executor.ExecuteCmd($"spawn_npc {Name}");
            WaitUntilRegisteredInMemory();
            IsSpawned = true;
        }

        public void TurnTo(float angle)
        {
            var saved = _memory.ReadXYZ();
            _memory.SetFacing(angle);
            _memory.SetPosition(saved.X, saved.Y, saved.Z);
        }

        private void WaitUntilRegisteredInMemory()
        {
            _memory.GetCurrentTargetLabel();
        }

        public event PropertyChangedEventHandler? PropertyChanged;
        private void OnPropertyChanged([CallerMemberName] string? n = null) =>
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(n));
    }
}
