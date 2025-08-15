import type { NextApiRequest, NextApiResponse } from 'next'
import fs from 'fs'
import path from 'path'

type StatsResponse = {
  neet: number
  jee: number
  pdf_universities: number
  total: number
  files_checked: string[]
}

export default function handler(req: NextApiRequest, res: NextApiResponse<StatsResponse | { error: string }>) {
  try {
    // In dev, process.cwd() is the frontend project root. The data folder is a sibling of frontend: ../data
    const dataDir = path.resolve(process.cwd(), '..', 'data')

    const files = {
      neet: path.join(dataDir, 'careers360_neet_colleges.json'),
      jee: path.join(dataDir, 'careers360_jee_colleges.json'),
      pdfSummary: path.join(dataDir, 'pdf_integration_summary.json'),
      pdfList: path.join(dataDir, 'pdf_ranking_colleges.json'),
    }

    let neet = 0
    let jee = 0
    let pdf_universities = 0

    if (fs.existsSync(files.neet)) {
      const neetData = JSON.parse(fs.readFileSync(files.neet, 'utf-8'))
      if (Array.isArray(neetData)) neet = neetData.length
    }

    if (fs.existsSync(files.jee)) {
      const jeeData = JSON.parse(fs.readFileSync(files.jee, 'utf-8'))
      if (Array.isArray(jeeData)) jee = jeeData.length
    }

    if (fs.existsSync(files.pdfSummary)) {
      const pdfSummary = JSON.parse(fs.readFileSync(files.pdfSummary, 'utf-8'))
      if (typeof pdfSummary?.total_colleges === 'number') {
        pdf_universities = pdfSummary.total_colleges
      }
    } else if (fs.existsSync(files.pdfList)) {
      const pdfList = JSON.parse(fs.readFileSync(files.pdfList, 'utf-8'))
      if (Array.isArray(pdfList)) pdf_universities = pdfList.length
    }

    const total = neet + jee + pdf_universities

    res.status(200).json({
      neet,
      jee,
      pdf_universities,
      total,
      files_checked: [files.neet, files.jee, files.pdfSummary, files.pdfList]
    })
  } catch (e: any) {
    res.status(200).json({
      neet: 0,
      jee: 0,
      pdf_universities: 0,
      total: 0,
      files_checked: []
    })
  }
}
