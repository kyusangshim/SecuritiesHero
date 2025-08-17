'use client'

import { useState, useEffect, useRef } from 'react'
import { Button } from './ui/button'
import { Edit3, X, AlertCircle, CheckCircle } from 'lucide-react'
import { saveDocumentContent, updateDocumentSection } from '../../lib/dart-viewer/document-actions'
import { getSectionKeyFromId } from '../../data/dart-viewer/mockDocumentData'

interface DocumentContentProps {
  htmlContent: string
  sectionId: string
  sectionName?: string
  sectionType?: 'part' | 'section-1' | 'section-2'
  onSectionModified?: (sectionId: string, updatedHTML: string) => void
  modifiedSections?: Set<string>
}

export function DocumentContent({ 
  htmlContent, 
  sectionId, 
  sectionName, 
  sectionType,
  onSectionModified,
  modifiedSections 
}: DocumentContentProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [hasError, setHasError] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [saveMessage, setSaveMessage] = useState('')
  const [originalHtml, setOriginalHtml] = useState('')
  const [currentHtml, setCurrentHtml] = useState('')
  const iframeRef = useRef<HTMLIFrameElement>(null)

  // 섹션이 변경될 때마다 편집 모드 초기화
  useEffect(() => {
    setIsEditing(false)
    setSaveMessage('')
  }, [sectionId, sectionName])

  // HTML 컨텐츠가 변경될 때 iframe에 로드
  useEffect(() => {
    const loadContent = async () => {
      if (!htmlContent) {
        setHasError(true)
        return
      }

      setIsLoading(true)
      setHasError(false)

      try {
        let processedHtml = htmlContent

        // 섹션별 처리가 필요한 경우
        if (sectionName && sectionType && sectionType !== 'part') {
          const parser = new DOMParser()
          const doc = parser.parseFromString(htmlContent, 'text/html')
          
          let extractedContent = ''
          
          if (sectionType === 'section-1') {
            const section1Elements = doc.querySelectorAll('.section-1')
            for (const element of section1Elements) {
              if (element.getAttribute('data-section') === sectionName) {
                extractedContent = element.outerHTML
                break
              }
            }
          } else if (sectionType === 'section-2') {
            const section2Elements = doc.querySelectorAll('.section-2')
            for (const element of section2Elements) {
              if (element.getAttribute('data-section') === sectionName) {
                extractedContent = element.outerHTML
                break
              }
            }
          }
          
          if (extractedContent) {
            const head = doc.querySelector('head')?.outerHTML || ''
            processedHtml = `
              <!DOCTYPE html>
              <html lang="ko">
              ${head}
              <body>
                <div class="document-content">
                  ${extractedContent}
                </div>
              </body>
              </html>
            `
          }
        }

        // iframe에 HTML 컨텐츠 로드
        if (iframeRef.current) {
          const iframe = iframeRef.current
          const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document
          
          if (iframeDoc) {
            iframeDoc.open()
            iframeDoc.write(processedHtml)
            iframeDoc.close()
            
            setOriginalHtml(processedHtml)
            setCurrentHtml(processedHtml)
            
            // 로드 완료 후 읽기 전용 모드 설정
            setTimeout(() => {
              ensureReadOnlyMode(iframeDoc)
              setIsLoading(false)
            }, 100)
          }
        }
      } catch (error) {
        console.error('HTML 컨텐츠 로드 오류:', error)
        setHasError(true)
        setIsLoading(false)
      }
    }

    loadContent()
  }, [htmlContent, sectionId, sectionName, sectionType])

  // 읽기 전용 모드 보장 함수
  const ensureReadOnlyMode = (iframeDoc: Document) => {
    const body = iframeDoc.body
    if (body) {
      body.contentEditable = 'false'
      body.style.outline = 'none'
      body.style.outlineOffset = '0'
      
      // 기존 편집 스타일 제거
      const existingStyles = iframeDoc.querySelectorAll('style')
      existingStyles.forEach(style => {
        if (style.textContent?.includes('contenteditable')) {
          style.remove()
        }
      })
    }
  }

  const handleEdit = () => {
    if (!iframeRef.current) return
    
    const iframeDoc = iframeRef.current.contentDocument || iframeRef.current.contentWindow?.document
    if (!iframeDoc) return

    // 현재 HTML 내용 저장
    setOriginalHtml(iframeDoc.documentElement.outerHTML)
    
    // iframe 내용을 편집 가능하게 만들기
    const body = iframeDoc.body
    if (body) {
      body.contentEditable = 'true'
      body.style.outline = '2px dashed #3b82f6'
      body.style.outlineOffset = '4px'
      
      // 포커스 설정
      body.focus()
    }
    
    setIsEditing(true)
    setSaveMessage('')
  }

  const handleSave = async () => {
    if (!iframeRef.current) return
    
    setIsSaving(true)
    setSaveMessage('')
    
    try {
      const iframeDoc = iframeRef.current.contentDocument || iframeRef.current.contentWindow?.document
      if (!iframeDoc) return

      // 저장하기 전에 편집 관련 스타일과 속성 정리
      const body = iframeDoc.body
      if (body) {
        // contentEditable 속성 제거
        body.contentEditable = 'false'
        body.removeAttribute('contenteditable')
        
        // 편집 관련 인라인 스타일 제거
        body.style.outline = 'none'
        body.style.outlineOffset = '0'
      }
      
      // 정리된 HTML 내용 가져오기
      const editedHtml = iframeDoc.documentElement.outerHTML

      let result

      const sectionKey = getSectionKeyFromId(sectionId)

      if (sectionName && sectionType && sectionType !== 'part') {
        // 하위 섹션 업데이트: 상위 HTML 파일의 해당 섹션만 업데이트
        result = await updateDocumentSection(htmlContent, sectionName, sectionType, editedHtml, sectionId, sectionKey)
      } else {
        // 전체 페이지 저장
        result = await saveDocumentContent(sectionKey, editedHtml)
      }
      
      // DB 기반에서는 즉시 저장하지 않고 부모 컴포넌트에 알림
      // 실제 DB 저장은 "최종 저장" 버튼에서 일괄 처리
      setCurrentHtml(editedHtml)
      setOriginalHtml(editedHtml)
      setIsEditing(false)
      
      // 섹션이 수정되었음을 부모 컴포넌트에 알림 (업데이트된 HTML과 함께)
      if (onSectionModified) {
        onSectionModified(sectionId, editedHtml)
      }
      
      setSaveMessage('편집이 완료되었습니다. "최종 저장"을 눌러 DB에 저장하세요.')
      
      // 성공 메시지 자동 숨김
      setTimeout(() => {
        setSaveMessage('')
      }, 5000)

      window.location.reload()
      
    } catch (error) {
      console.error('편집 완료 오류:', error)
      setSaveMessage('편집 완료 중 오류가 발생했습니다.')
      
      // 에러 발생 시 편집 모드 복원
      const iframeDoc = iframeRef.current?.contentDocument || iframeRef.current?.contentWindow?.document
      const body = iframeDoc?.body
      if (body) {
        body.contentEditable = 'true'
        body.style.outline = '2px dashed #3b82f6'
        body.style.outlineOffset = '4px'
      }
    } finally {
      setIsSaving(false)
    }
  }

  const handleCancel = () => {
    if (!iframeRef.current) return
    
    const iframeDoc = iframeRef.current.contentDocument || iframeRef.current.contentWindow?.document
    if (iframeDoc && originalHtml) {
      // 원본 HTML로 복원
      iframeDoc.open()
      iframeDoc.write(originalHtml)
      iframeDoc.close()
      
      // 읽기 전용 모드 보장
      setTimeout(() => {
        ensureReadOnlyMode(iframeDoc)
      }, 100)
    }
    
    setIsEditing(false)
    setSaveMessage('')
  }

  const handleImageInsert = () => {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = 'image/*'

    input.onchange = async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0]
      if (!file) return

      const reader = new FileReader()
      reader.onload = () => {
        const imgSrc = reader.result as string

        // iframe 안의 커서 위치에 이미지 삽입
        const iframeDoc = iframeRef.current?.contentDocument
        if (!iframeDoc) return

        const selection = iframeDoc.getSelection()
        if (!selection || !selection.rangeCount) return

        const img = iframeDoc.createElement('img')
        img.src = imgSrc
        img.style.maxWidth = '100%'
        img.style.height = 'auto'

        const range = selection.getRangeAt(0)
        range.insertNode(img)
      }
      reader.readAsDataURL(file)
    }

    input.click()
  }

  // HTML 컨텐츠가 비어있는 경우 처리
  if (!htmlContent) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <AlertCircle className="w-8 h-8 text-gray-400 mx-auto mb-2" />
          <p className="text-gray-600 text-sm">선택된 섹션의 내용이 없습니다.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full relative">
      {/* 편집 도구바 */}
      <div className="absolute top-4 right-4 z-20 flex items-center gap-2">
        {isEditing ? (
          <div className="flex items-center gap-2">
            {/* 이미지 추가 버튼 */}
            <Button
              onClick={handleImageInsert}
              size="sm"
              variant="outline"
              className="bg-white shadow-md hover:bg-gray-50"
            >
              이미지 추가
            </Button>
            <Button
              onClick={handleSave}
              size="sm"
              disabled={isSaving}
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              <CheckCircle className="w-4 h-4 mr-1" />
              {isSaving ? '편집 완료 중...' : '편집 완료'}
            </Button>

            <Button
              onClick={handleCancel}
              size="sm"
              variant="outline"
              className="bg-white"
            >
              <X className="w-4 h-4 mr-1" />
              취소
            </Button>
          </div>
        ) : (
          <Button
            onClick={handleEdit}
            size="sm"
            variant="outline"
            className="bg-white shadow-md hover:bg-gray-50"
          >
            <Edit3 className="w-4 h-4 mr-1" />
            편집 시작
          </Button>
        )}
      </div>

      {/* 편집 모드 안내 */}
      {isEditing && (
        <div className="absolute top-16 right-4 z-20 bg-blue-100 text-blue-800 p-3 rounded-md shadow-md max-w-sm">
          <div className="flex items-center gap-2">
            <Edit3 className="w-4 h-4" />
            <span className="text-sm font-medium">편집 중</span>
          </div>
          <p className="text-xs mt-1">
            문서 내용을 직접 클릭하여 수정할 수 있습니다.
          </p>
        </div>
      )}

      {/* 저장 메시지 */}
      {saveMessage && (
        <div className={`absolute ${isEditing ? 'top-32' : 'top-16'} right-4 z-20 p-3 rounded-md shadow-md max-w-sm transition-opacity duration-300 ${
          saveMessage.includes('완료') || saveMessage.includes('성공')
            ? 'bg-green-100 text-green-800 border border-green-200' 
            : 'bg-red-100 text-red-800 border border-red-200'
        }`}>
          <div className="flex items-center gap-2">
            {saveMessage.includes('완료') || saveMessage.includes('성공') ? (
              <CheckCircle className="w-4 h-4" />
            ) : (
              <AlertCircle className="w-4 h-4" />
            )}
            <span className="text-sm">{saveMessage}</span>
          </div>
        </div>
      )}

      {/* 로딩 상태 */}
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
            <p className="text-gray-600 text-sm">문서를 불러오는 중...</p>
          </div>
        </div>
      )}
      
      {/* 에러 상태 */}
      {hasError && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <AlertCircle className="w-8 h-8 text-gray-400 mx-auto mb-2" />
            <p className="text-red-600 text-sm mb-2">문서를 불러올 수 없습니다.</p>
            <button 
              onClick={() => {
                setHasError(false)
                setIsLoading(true)
              }}
              className="text-blue-600 text-sm hover:underline"
            >
              다시 시도
            </button>
          </div>
        </div>
      )}

      {/* 문서 내용 */}
      <iframe
        ref={iframeRef}
        key={`${sectionId}-${sectionName || 'full'}-${htmlContent.length}`}
        className="w-full h-full border-0"
        title="Document Content"
        sandbox="allow-same-origin allow-scripts"
        style={{ display: isLoading || hasError ? 'none' : 'block' }}
      />
    </div>
  )
}