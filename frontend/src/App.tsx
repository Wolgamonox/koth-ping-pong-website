import { Box } from '@mantine/core';
import { ThemeProvider } from './ThemeProvider';

export default function App() {
  return (
    <ThemeProvider>
      <Box>Gekki</Box>
    </ThemeProvider>
  );
}