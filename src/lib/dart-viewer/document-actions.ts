'use server'

import { writeFile, readFile } from 'fs/promises'
import { join } from 'path'
import { markSectionAsModified } from './version-actions'
import prettier from 'prettier'

export async function saveDocumentContent(filePath: string, content: string) {
  try {
    const fullPath = join(process.cwd(), 'public', filePath.replace('/documents/', 'documents/'))
    await writeFile(fullPath, content, 'utf-8')
    return { success: true, message: '문서가 성공적으로 저장되었습니다.' }
  } catch (error) {
    console.error('Error saving document:', error)
    return { success: false, message: '문서 저장 중 오류가 발생했습니다.' }
  }
}

export async function updateDocumentSection(
  filePath: string, 
  sectionName: string, 
  sectionType: 'section-1' | 'section-2', 
  updatedContent: string,
  sectionId?: string
) {
  try {
    const fullPath = join(process.cwd(), 'public', filePath.replace('/documents/', 'documents/'))
    
    // 원본 HTML 파일 읽기
    const originalHtml = await readFile(fullPath, 'utf-8')
    
    // 업데이트된 내용에서 실제 콘텐츠 추출
    const contentMatch = updatedContent.match(
      `<div class="${sectionType}"[^>]*data-section="${sectionName}"[^>]*>([\\s\\S]*?)<\\/div>(?=\\s*(?:<div class="${sectionType}"|<div class="section-divider"|<\\/div>|$))`
    )

    if (!contentMatch) {
      console.log('No document-content found in updated content')
      return { success: false, message: '업데이트할 내용을 찾을 수 없습니다.' }
    }
    
    let newContent = contentMatch[1].trim()
    
    // 다양한 패턴으로 섹션 찾기 시도
    const patterns = [
      // 패턴 1: data-section이 먼저 오는 경우
      new RegExp(`<div class="${sectionType}"[^>]*data-section="${sectionName}"[^>]*>([\\s\\S]*?)<\\/div>(?=\\s*(?:<div class="${sectionType}"|<div class="section-divider"|<\\/div>|$))`, 'i'),
      
      // 패턴 2: data-section이 나중에 오는 경우  
      new RegExp(`<div[^>]*data-section="${sectionName}"[^>]*class="${sectionType}"[^>]*>([\\s\\S]*?)<\\/div>(?=\\s*(?:<div class="${sectionType}"|<div class="section-divider"|<\\/div>|$))`, 'i'),
      
      // 패턴 3: 속성 순서 상관없이
      new RegExp(`<div[^>]*(?:class="${sectionType}"[^>]*data-section="${sectionName}"|data-section="${sectionName}"[^>]*class="${sectionType}")[^>]*>([\\s\\S]*?)<\\/div>(?=\\s*(?:<div|<\\/div>|$))`, 'i'),
      
      // 패턴 4: 더 간단한 패턴
      new RegExp(`data-section="${sectionName}"[^>]*>([\\s\\S]*?)<\\/div>`, 'i')
    ]
    
    let match = null
    let usedPatternIndex = -1
    
    for (let i = 0; i < patterns.length; i++) {
      match = originalHtml.match(patterns[i])
      if (match) {
        usedPatternIndex = i
        console.log(`Found match with pattern ${i + 1}`)
        break
      }
    }
    
    if (!match) {
      console.log('No section found with any pattern')
      
      // 디버깅을 위해 원본 HTML에서 해당 섹션 이름이 있는지 확인
      const sectionExists = originalHtml.includes(`data-section="${sectionName}"`)
      console.log('Section exists in HTML:', sectionExists)
      
      if (sectionExists) {
        // 섹션이 존재하지만 매칭되지 않는 경우, 해당 부분의 HTML 구조 출력
        const lines = originalHtml.split('\n')
        const sectionLineIndex = lines.findIndex(line => line.includes(`data-section="${sectionName}"`))
        if (sectionLineIndex !== -1) {
          console.log('Section context:')
          for (let i = Math.max(0, sectionLineIndex - 2); i <= Math.min(lines.length - 1, sectionLineIndex + 5); i++) {
            console.log(`${i}: ${lines[i]}`)
          }
        }
      }
      
      return { success: false, message: '업데이트할 섹션을 찾을 수 없습니다.' }
    }
    
    // 매칭된 패턴으로 교체
    const updatedHtml = originalHtml.replace(patterns[usedPatternIndex], (fullMatch) => {
      // 전체 매치에서 내용 부분만 교체
      const openTagMatch = fullMatch.match(/^<div[^>]*>/i)
      if (openTagMatch) {
        return `${openTagMatch[0]}\n${newContent}\n</div>`
      }
      return fullMatch
    })

    const formattedHtml = await prettier.format(updatedHtml, { parser: 'html' })
    
    console.log('Section updated successfully')
    
    // 업데이트된 HTML 저장
    await writeFile(fullPath, formattedHtml, 'utf-8')
    
    // 섹션을 수정됨으로 표시 (버전 관리)
    if (sectionId) {
      await markSectionAsModified(sectionId)
    }
    
    return { success: true, message: '섹션이 성공적으로 업데이트되었습니다.' }
  } catch (error) {
    console.error('Error updating document section:', error)
    return { success: false, message: '섹션 업데이트 중 오류가 발생했습니다.' }
  }
}

export async function getDocumentContent(filePath: string) {
  try {
    const fullPath = join(process.cwd(), 'public', filePath.replace('/documents/', 'documents/'))
    const content = await readFile(fullPath, 'utf-8')
    return { success: true, content }
  } catch (error) {
    console.error('Error reading document:', error)
    return { success: false, content: '' }
  }
}
