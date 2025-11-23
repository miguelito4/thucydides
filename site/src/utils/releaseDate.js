/**
 * Calculate if a given day number has been released yet
 * Day 1 releases on January 1, 2026
 * Each subsequent day releases at midnight UTC
 */

const START_DATE = new Date('2025-11-26T00:00:00Z'); // Tuesday, November 26, 2025

export function isReleased(dayNumber) {
  const releaseDate = getReleaseDate(dayNumber);
  const now = new Date();
  return now >= releaseDate;
}

export function getReleaseDate(dayNumber) {
  // dayNumber is 1-indexed (Day 1, Day 2, etc.)
  // But chunk_index in data is 0-indexed
  const daysToAdd = dayNumber - 1;
  const releaseDate = new Date(START_DATE);
  releaseDate.setDate(releaseDate.getDate() + daysToAdd);
  return releaseDate;
}

export function getReleasedDayCount() {
  const now = new Date();
  const diffTime = now - START_DATE;
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  return Math.max(0, diffDays + 1); // +1 because Day 1 releases on day 0
}

export function formatDate(date) {
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
}

export function getProgressPercentage(dayNumber, totalDays = 506) {
  return Math.round((dayNumber / totalDays) * 100);
}
