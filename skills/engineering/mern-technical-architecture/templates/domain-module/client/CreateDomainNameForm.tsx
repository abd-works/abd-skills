/**
 * CreateDomainNameForm.tsx — Form component for creating a new domain entity.
 *
 * Validates input using the Zod schema from shared/ (same schema the server
 * uses at the repository boundary). On successful submission, calls the
 * create API function and notifies the parent via onCreated callback.
 *
 * Include this form only when the specs define a user-facing create action.
 * Some POST endpoints may exist only for system-to-system workflows and should
 * not automatically produce a corresponding UI control.
 */
import { useState } from 'react';
import { DomainName, CreateDomainNameInputSchema } from '@appName/domainName-shared';
import { createDomainName } from './domainName.api';

interface CreateDomainNameFormProps {
  onCreated: (entity: DomainName) => void;
}

export function CreateDomainNameForm({ onCreated }: CreateDomainNameFormProps) {
  const [name, setName] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setError(null);

    const input = { name: name.trim() };
    const validation = CreateDomainNameInputSchema.safeParse(input);
    if (!validation.success) {
      setError(validation.error.issues[0].message);
      return;
    }

    try {
      const created = await createDomainName(validation.data);
      onCreated(created);
      setName('');
    } catch {
      setError('Failed to create');
    }
  };

  return (
    <form className="create-domainName-form" onSubmit={handleSubmit}>
      <h2>Create DomainName</h2>
      <div className="form-field">
        <label htmlFor="domainName-name">Name</label>
        <input
          id="domainName-name"
          type="text"
          value={name}
          onChange={(e: any) => setName(e.target.value)}
        />
      </div>
      {error && <p className="error">{error}</p>}
      <button type="submit" disabled={!name.trim()}>Save</button>
    </form>
  );
}
