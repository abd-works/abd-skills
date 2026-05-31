import React from 'react';

interface RequireStoreEmployeeProps {
  isEmployee: boolean;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

/** Employee gate — customers receive fallback (403 message or redirect). */
export function RequireStoreEmployee({
  isEmployee,
  children,
  fallback = (
    <p data-testid="employee-access-denied" role="alert">
      stock maintenance unavailable
    </p>
  ),
}: RequireStoreEmployeeProps) {
  if (!isEmployee) {
    return <>{fallback}</>;
  }
  return <>{children}</>;
}
