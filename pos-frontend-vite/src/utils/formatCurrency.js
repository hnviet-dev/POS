/**
 * Format a number with $ symbol
 * @param {number|null|undefined} amount
 * @returns {string}  e.g. "$1.250.000"
 */
export const fmtVND = (amount) =>
  `$${(amount || 0).toLocaleString("vi-VN")}`;
