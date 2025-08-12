// calculationTest.js
// Standalone script to validate FTE, Leave FTE, Cost Revenue, and Total Revenue calculations
// Mirrors backend/frontend logic for 'Total FTE' and 'Leave Summary' tabs

function calculateAll({
  year, monthIdx, rateCard, assignmentStart, billableStart, billableEnd, leaveDates = [], holidays
}) {
  // Calculate month boundaries
  const monthStart = new Date(Date.UTC(year, monthIdx, 1));
  const monthEnd = new Date(Date.UTC(year, monthIdx + 1, 0));
  // Assignment/billing windows (use billing end as assignment end)
  let asgStart = assignmentStart && assignmentStart > monthStart ? assignmentStart : monthStart;
  let asgEnd = billableEnd && billableEnd < monthEnd ? billableEnd : monthEnd; // use billing end as assignment end
  let billStart = billableStart && billableStart > monthStart ? billableStart : monthStart;
  let billEnd = billableEnd && billableEnd < monthEnd ? billableEnd : monthEnd;

  function isWorkingDay(d) {
    const day = d.getUTCDay();
    const dateStr = d.toISOString().slice(0, 10);
    return day !== 0 && day !== 6 && !holidays.includes(dateStr);
  }
  function countWorkingDays(start, end) {
    let count = 0;
    for (let d = new Date(start); d <= end; d.setUTCDate(d.getUTCDate() + 1)) {
      if (isWorkingDay(d)) count++;
    }
    return count;
  }
  function countLeaveDaysInWindow(start, end) {
    return leaveDates.filter(ld => {
      const d = new Date(ld);
      return d >= start && d <= end && isWorkingDay(d);
    }).length;
  }

  // Pre-billing NBL window (clamped)
  let preNBLStart = asgStart;
  let preNBLEnd = billStart > asgStart ? new Date(Math.min(billStart.getTime() - 86400000, monthEnd.getTime())) : new Date(Math.min(asgStart.getTime(), monthEnd.getTime()));
  let preNBLDays = 0, leaveInPreNBL = 0;
  if (preNBLEnd >= preNBLStart) {
    preNBLDays = countWorkingDays(preNBLStart, preNBLEnd);
    leaveInPreNBL = countLeaveDaysInWindow(preNBLStart, preNBLEnd);
  }
  // Post-billing NBL window (clamped)
  let postNBLStart = billEnd < asgEnd ? new Date(Math.max(billEnd.getTime() + 86400000, monthStart.getTime())) : new Date(Math.max(asgEnd.getTime(), monthStart.getTime()));
  let postNBLEnd = asgEnd;
  let postNBLDays = 0, leaveInPostNBL = 0;
  if (postNBLEnd >= postNBLStart) {
    postNBLDays = countWorkingDays(postNBLStart, postNBLEnd);
    leaveInPostNBL = countLeaveDaysInWindow(postNBLStart, postNBLEnd);
  }
  const nblDays = (preNBLDays - leaveInPreNBL) + (postNBLDays - leaveInPostNBL);
  const totalMonthWorkingDays = countWorkingDays(monthStart, monthEnd);
  const nonBillableFte = totalMonthWorkingDays > 0 ? nblDays / totalMonthWorkingDays : 0;

  // Billed FTE logic
  let billedStart = billableStart && billableStart > monthStart ? billableStart : monthStart;
  let billedEnd = billableEnd && billableEnd < monthEnd ? billableEnd : monthEnd;
  let billedDays = 0;
  for (let d = new Date(monthStart); d <= monthEnd; d.setUTCDate(d.getUTCDate() + 1)) {
    if (isWorkingDay(d)) {
      if (d >= billedStart && d <= billedEnd) billedDays++;
    }
  }
  const leaveDaysInBillingPeriod = leaveDates.filter(ld => {
    const d = new Date(ld);
    return d >= billedStart && d <= billedEnd && isWorkingDay(d);
  }).length;
  const actualBilledDays = Math.max(0, billedDays - leaveDaysInBillingPeriod);
  const billedFte = totalMonthWorkingDays > 0 ? (actualBilledDays / totalMonthWorkingDays) : 0;

  // Leave FTE/Total FTE
  let leaveDays = leaveDates.filter(ld => {
    const d = new Date(ld);
    return d >= monthStart && d <= monthEnd && isWorkingDay(d);
  }).length;
  let totalWorkingDays = countWorkingDays(asgStart, asgEnd);
  let actualWorkingDays = Math.max(0, totalWorkingDays - leaveDays);
  const costRevenue = `£${(rateCard * actualWorkingDays).toFixed(2)}`;
  const totalRevenue = `$${((rateCard * actualWorkingDays) * 1.29).toFixed(2)}`;
  const totalFte = totalWorkingDays > 0 ? (actualWorkingDays / totalWorkingDays) : 0;
  const leaveFte = totalWorkingDays > 0 ? (leaveDays / totalWorkingDays) : 0;

  return {
    totalWorkingDays,
    actualWorkingDays,
    costRevenue,
    totalRevenue,
    totalFte,
    leaveFte,
    windowStart,
    windowEnd
  };
}

function printTestResult(label, res, expected) {
  console.log('--- ' + label + ' ---');
  console.log(`Assignment Window: ${res.windowStart.toISOString().slice(0,10)} to ${res.windowEnd.toISOString().slice(0,10)}`);
  console.log(`Total Working Days: ${res.totalWorkingDays}`);
  console.log(`Leave Days: ${expected.leaveDays}`);
  console.log(`Actual Working Days: ${res.actualWorkingDays}`);
  console.log(`Cost Revenue: ${res.costRevenue}`);
  console.log(`Total Revenue: ${res.totalRevenue}`);
  console.log(`Total FTE: ${res.totalFte.toFixed(2)}`);
  console.log(`Leave FTE: ${res.leaveFte.toFixed(2)}`);
  if (expected.expect) {
    Object.entries(expected.expect).forEach(([k, v]) => {
      if (typeof v === 'number') {
        const actual = (typeof res[k] === 'number') ? res[k] : parseFloat(String(res[k]).replace(/[^\d.\-]/g, ''));
        console.log(`  Expect ${k}: ${v} => ${Math.abs(actual - v) < 0.01 ? 'PASS' : 'FAIL'}`);
      } else {
        console.log(`  Expect ${k}: ${v} => ${res[k] === v ? 'PASS' : 'FAIL'}`);
      }
    });
  }
  console.log('-------------------------\n');
}

// --- Test Cases ---
const holidays = ['2025-01-01']; // New Year's Day
const year = 2025;
const rateCard = 10000;

const tests = [
  {
    label: 'Full Month, 2 Leave Days',
    year,
    monthIdx: 0, // Jan
    rateCard,
    assignmentStart: new Date(Date.UTC(2025, 0, 1)),
    billableStart: new Date(Date.UTC(2025, 0, 1)),
    billableEnd: new Date(Date.UTC(2025, 0, 31)),
    leaveDays: 2,
    holidays,
    expect: {
      totalWorkingDays: 23,
      actualWorkingDays: 21,
      costRevenue: '£210000.00',
      totalRevenue: '$270900.00',
      totalFte: 0.91,
      leaveFte: 0.09
    }
  },
  {
    label: 'Partial Month (mid-start), 0 Leave',
    year,
    monthIdx: 0, // Jan
    rateCard,
    assignmentStart: new Date(Date.UTC(2025, 0, 15)),
    billableStart: new Date(Date.UTC(2025, 0, 15)),
    billableEnd: new Date(Date.UTC(2025, 0, 31)),
    leaveDays: 0,
    holidays,
    expect: {
      totalWorkingDays: 13,
      actualWorkingDays: 13,
      costRevenue: '£130000.00',
      totalRevenue: '$167700.00',
      totalFte: 1.00,
      leaveFte: 0.00
    }
  },
  {
    label: 'All Leave',
    year,
    monthIdx: 0, // Jan
    rateCard,
    assignmentStart: new Date(Date.UTC(2025, 0, 1)),
    billableStart: new Date(Date.UTC(2025, 0, 1)),
    billableEnd: new Date(Date.UTC(2025, 0, 31)),
    leaveDays: 23,
    holidays,
    expect: {
      totalWorkingDays: 23,
      actualWorkingDays: 0,
      costRevenue: '£0.00',
      totalRevenue: '$0.00',
      totalFte: 0.00,
      leaveFte: 1.00
    }
  },
  {
    label: 'No Working Days (weekend only)',
    year,
    monthIdx: 1, // Feb (simulate assignment only on weekends)
    rateCard,
    assignmentStart: new Date(Date.UTC(2025, 1, 1)),
    billableStart: new Date(Date.UTC(2025, 1, 1)),
    billableEnd: new Date(Date.UTC(2025, 1, 2)),
    leaveDays: 0,
    holidays: [],
    expect: {
      totalWorkingDays: 0,
      actualWorkingDays: 0,
      costRevenue: '£0.00',
      totalRevenue: '$0.00',
      totalFte: 0.00,
      leaveFte: 0.00
    }
  }
];

tests.forEach(test => {
  const res = calculateAll(test);
  printTestResult(test.label, res, test);
});

// Compare these with your backend output for the same sample data.
