'use client';

import React from 'react';

interface Branch {
  id: string;
  name: string;
}

interface BranchSelectorProps {
  branches: Branch[];
  selectedBranch: string;
  onBranchChange: (branchId: string) => void;
}

const BranchSelector = ({
  branches,
  selectedBranch,
  onBranchChange,
}: BranchSelectorProps) => {
  return (
    <div className="w-full max-w-xs">
      <label htmlFor="branch-select" className="block text-sm font-medium text-gray-700 mb-2">
        Seleccionar Sucursal
      </label>
      <select
        id="branch-select"
        value={selectedBranch}
        onChange={(e) => onBranchChange(e.target.value)}
        className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
      >
        {branches.map((branch) => (
          <option key={branch.id} value={branch.id}>
            {branch.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default BranchSelector;