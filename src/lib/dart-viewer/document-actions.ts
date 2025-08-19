'use server'

import { markSectionAsModified } from './version-actions'
import prettier from "prettier/standalone"
import parserHtml from "prettier/plugins/html"

export async function saveDocumentContent(sectionKey: string, content: string) {
  try {
    const response = await fetch('http://localhost:8000/versions/editing', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: 1, 
        description: '편집중인 버전',
        createdAt: new Date().toISOString(),
        sectionsData: {
          [sectionKey]: content
        }
      })
    })

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    return { success: true, message: "편집 버전이 저장되었습니다." }
  } catch (error) {
    console.error('Error saving document content to DB:', error)
    return { success: false, message: 'DB 저장 중 오류가 발생했습니다.' }
  }
}


export async function updateDocumentSection(
  htmlContent: string,
  sectionName: string,
  sectionType: 'section-1' | 'section-2',
  updatedContent: string,
  sectionId: string,
  sectionKey: string
) {
  try {
    // updatedContent에서 해당 섹션 요소 추출
    const updatedDoc = new DOMParser().parseFromString(updatedContent, 'text/html')
    const selector = `.${sectionType}[data-section="${sectionName}"]`
    const updatedSection = updatedDoc.querySelector(selector)

    if (!updatedSection) {
      return { success: false, message: '업데이트할 섹션을 찾을 수 없습니다.' }
    }

    // 원본 HTML에서 해당 섹션 교체
    const originalDoc = new DOMParser().parseFromString(htmlContent, 'text/html')
    const originalSection = originalDoc.querySelector(selector)

    if (!originalSection) {
      return { success: false, message: '원본에서 섹션을 찾을 수 없습니다.' }
    }

    // 통째로 교체
    originalSection.outerHTML = updatedSection.outerHTML
    const finalHtml = `<!DOCTYPE html>\n${originalDoc.documentElement.outerHTML}`

    // HTML 문자열로 변환
    const updatedHtml = await prettier.format(finalHtml, {
      parser: "html",
      plugins: [parserHtml],
    })

    // DB 저장
    const response = await fetch('http://localhost:8000/versions/editing', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: 1,
        description: '편집중인 버전',
        createdAt: new Date().toISOString(),
        sectionsData: {
          [sectionKey]: updatedHtml
        }
      })
    })

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)

    if (sectionId) {
      await markSectionAsModified(sectionId)
    }

    return { success: true, message: "편집 버전이 저장되었습니다." }
  } catch (error) {
    console.error('Error updating document section:', error)
    return { success: false, message: '섹션 업데이트 중 오류가 발생했습니다.' }
  }
}

