using Prism.Commands;
using Prism.Mvvm;

namespace Module.HeroVirtualTabletop.Characters
{
    public class CharacterViewModel : BindableBase
    {
        private readonly Character _character;

        public CharacterViewModel(Character character)
        {
            _character = character;
            SpawnCommand = new DelegateCommand(() => _character.Spawn());
            TurnCommand = new DelegateCommand<float?>(
                angle => _character.TurnTo(angle!.Value));
        }

        public string CharacterName => _character.Name;
        public bool IsSpawned => _character.IsSpawned;

        public DelegateCommand SpawnCommand { get; }
        public DelegateCommand<float?> TurnCommand { get; }
    }
}
