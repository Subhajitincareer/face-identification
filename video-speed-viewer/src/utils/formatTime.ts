export function formatTime(seconds: number | undefined | null): string {
  if (seconds === undefined || seconds === null || isNaN(seconds) || seconds < 0) {
    return '00:00';
  }

  const roundedSeconds = Math.floor(seconds);
  const m = Math.floor(roundedSeconds / 60);
  const s = roundedSeconds % 60;

  const paddedM = m.toString().padStart(2, '0');
  const paddedS = s.toString().padStart(2, '0');

  return `${paddedM}:${paddedS}`;
}
