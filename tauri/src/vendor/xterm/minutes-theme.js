// Shared xterm.js theme for Artemis Paysages — used by both index.html (Recall panel)
// and terminal.html (standalone fallback).
// Palette aligned with styles/theme-tokens.css (olive Paysages + neutres Artemis).
function getMinutesTheme(isDark) {
  if (isDark) {
    // Dark Artemis — fond sombre olive, accent olive éclairci
    return {
      background: '#1A1C16',
      foreground: '#EDEAD8',
      cursor: '#9FB455',
      cursorAccent: '#1A1C16',
      selectionBackground: 'rgba(159, 180, 85, 0.22)',
      selectionForeground: '#EDEAD8',
      black: '#1A1C16',
      red: '#E06B5E',
      green: '#2E8A66',
      yellow: '#D4832A',
      blue: '#9FB455',
      magenta: '#8F7B70',
      cyan: '#7FAEA0',
      white: '#EDEAD8',
      brightBlack: '#5F6358',
      brightRed: '#EB8478',
      brightGreen: '#4FA77F',
      brightYellow: '#E2A24F',
      brightBlue: '#B4C96C',
      brightMagenta: '#A8958B',
      brightCyan: '#9ED6C9',
      brightWhite: '#F8F6F1',
    };
  }

  // Light Artemis — fond crème, accent olive
  return {
    background: '#F8F6F1',
    foreground: '#22262A',
    cursor: '#7B9237',
    cursorAccent: '#F8F6F1',
    selectionBackground: 'rgba(123, 146, 55, 0.18)',
    selectionForeground: '#22262A',
    black: '#22262A',
    red: '#A51F18',
    green: '#0C5D40',
    yellow: '#AD6200',
    blue: '#7B9237',
    magenta: '#68544B',
    cyan: '#4F7E72',
    white: '#EEEAE0',
    brightBlack: '#6D757E',
    brightRed: '#C04A3F',
    brightGreen: '#2E7D54',
    brightYellow: '#C88932',
    brightBlue: '#9AAF4F',
    brightMagenta: '#8F7667',
    brightCyan: '#6A9E92',
    brightWhite: '#FFFFFF',
  };
}

const minutesThemeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

window.getMinutesTheme = getMinutesTheme;
window.MINUTES_XTERM_THEME_QUERY = minutesThemeMediaQuery;
window.MINUTES_XTERM_THEME = getMinutesTheme(minutesThemeMediaQuery.matches);
