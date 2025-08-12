// Simple CSV export utility for arrays of objects
export function exportToCsv(filename, columns, rows) {
  columns = Array.isArray(columns) ? columns : [];
  rows = Array.isArray(rows) ? rows : [];
  const escape = (val) => '"' + String(val).replace(/"/g, '""') + '"';
  const header = columns.map(col => escape(col.headerName || col.field)).join(',');
  const csvRows = rows.map(row => columns.map(col => escape(row[col.field] ?? '')).join(',')).join('\r\n');
  const csvContent = [header, ...csvRows].join('\r\n');
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  setTimeout(() => {
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, 100);
}
