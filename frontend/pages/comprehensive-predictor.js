import React from 'react';
import Head from 'next/head';
import CollegePredictor from '../components/CollegePredictor';

export default function ComprehensivePredictor() {
  return (
    <>
      <Head>
        <title>Comprehensive College Predictor - Collink</title>
        <meta name="description" content="Complete college prediction with data from PDF and Careers360 - No backend limitations" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <CollegePredictor />
    </>
  );
}
