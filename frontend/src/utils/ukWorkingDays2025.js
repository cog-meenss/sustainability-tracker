// Returns an object: { Jan: 23, Feb: 20, ... } for UK working days in 2025
// Excludes weekends and UK public holidays (England & Wales)
export function getUKWorkingDays2025() {
  const holidays = [
    '2025-01-01', // New Year's Day
    '2025-04-18', // Good Friday
    '2025-04-21', // Easter Monday
    '2025-05-05', // Early May bank holiday
    '2025-05-26', // Spring bank holiday
    '2025-08-25', // Summer bank holiday
    '2025-12-25', // Christmas Day
    '2025-12-26', // Boxing Day
  ];
  const isHoliday = date => holidays.includes(date.toISOString().slice(0,10));
  const monthNames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const result = {};
  for (let m = 0; m < 12; m++) {
    let count = 0;
    for (let d = 1; d <= 31; d++) {
      const date = new Date(2025, m, d);
      if (date.getMonth() !== m) break;
      const day = date.getDay();
      if (day === 0 || day === 6) continue; // skip weekends
      if (isHoliday(date)) continue;
      count++;
    }
    result[monthNames[m]] = count;
  }
  return result;
}
