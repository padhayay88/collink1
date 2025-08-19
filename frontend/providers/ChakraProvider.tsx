'use client';

import { ChakraProvider as BaseChakraProvider } from '@chakra-ui/react';

export function ChakraProvider({ children }: { children: React.ReactNode }) {
  return (
    <BaseChakraProvider>
      {children}
    </BaseChakraProvider>
  );
}
