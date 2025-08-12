import { useState, useRef, useEffect, useCallback } from 'react'
import { ChevronLeft, ChevronRight, Loader2, Plus } from 'lucide-react'
import { Button } from './ui/button'
import { TableOfContents } from './table-of-contents'
import { DocumentContent } from './document-content'
import { VersionSelector } from './version-selector'
import { 
  getProjectState, 
  createNewVersion, 
  switchToVersion, 
  getVersionList, 
  initializeProject, 
  getSectionHTML,
  getVersionSections,
  type VersionInfo 
} from '../../lib/dart-viewer/version-actions'
import { mockDocumentData, DocumentSection, getSectionKeyFromId } from '../../data/dart-viewer/mockDocumentData'

export function DocumentViewer() {
  const [selectedSection, setSelectedSection] = useState<string>('1')
  const [isLeftPanelCollapsed, setIsLeftPanelCollapsed] = useState(false)
  const [leftPanelWidth, setLeftPanelWidth] = useState(25)
  const [isDragging, setIsDragging] = useState(false)
  const [startX, setStartX] = useState(0)
  const [startWidth, setStartWidth] = useState(25)
  const [currentVersion, setCurrentVersion] = useState('v0')
  const [versions, setVersions] = useState<VersionInfo[]>([])
  const [modifiedSections, setModifiedSections] = useState<Set<string>>(new Set())
  const [isCreatingVersion, setIsCreatingVersion] = useState(false)
  const [currentSectionHTML, setCurrentSectionHTML] = useState<string>('')
  const [isLoadingSection, setIsLoadingSection] = useState(false)
  const [versionSectionsData, setVersionSectionsData] = useState<Record<string, string>>({})
  const containerRef = useRef<HTMLDivElement>(null)
  const [expandedSections, setExpandedSections] = useState<Set<string>>(
    new Set(['3', '6', '7', '14', '21', '22', '28', '36', '47', '50', '55', '60', '66'])
  )


  // 프로젝트 상태 로드
  useEffect(() => {
    const loadProjectState = async () => {
      try {
        // 프로젝트 초기화 확인
        await initializeProject()
        
        const state = await getProjectState()
        console.log(state)
        setCurrentVersion(state.currentVersion)
        setModifiedSections(state.modifiedSections)
        
        const versionList = await getVersionList()
        setVersions(versionList)
        
        // 현재 버전의 모든 섹션 데이터 로드
        const sectionsData = await getVersionSections(state.currentVersion)
        setVersionSectionsData(sectionsData)
      } catch (error) {
        console.error('프로젝트 상태 로드 오류:', error)
      }
    }
    
    loadProjectState()
  }, [])

  // 선택된 섹션이 변경될 때 해당 섹션의 HTML 로드
  useEffect(() => {
    const loadSectionHTML = async () => {
      if (!selectedSection || !currentVersion) return
      
      setIsLoadingSection(true)
      
      try {
        // 섹션 ID를 섹션 키로 변환
        const sectionKey = getSectionKeyFromId(selectedSection)
        
        // 먼저 메모리에 캐시된 데이터 확인
        if (versionSectionsData[sectionKey]) {
          setCurrentSectionHTML(versionSectionsData[sectionKey])
        } else {
          // 캐시에 없으면 DB에서 가져오기
          const html = await getSectionHTML(currentVersion, sectionKey)
          setCurrentSectionHTML(html)
          
          // 캐시 업데이트
          setVersionSectionsData(prev => ({
            ...prev,
            [sectionKey]: html
          }))
        }
      } catch (error) {
        console.error('섹션 HTML 로드 오류:', error)
        setCurrentSectionHTML('')
      } finally {
        setIsLoadingSection(false)
      }
    }
    
    loadSectionHTML()
  }, [selectedSection, currentVersion, versionSectionsData])

  // 버전이 변경될 때 새로운 버전의 섹션 데이터 로드
  useEffect(() => {
    const loadVersionData = async () => {
      if (!currentVersion) return
      
      try {
        const sectionsData = await getVersionSections(currentVersion)
        setVersionSectionsData(sectionsData)
        
        // 현재 선택된 섹션의 HTML도 업데이트
        const selectedSectionKey = getSectionKeyFromId(selectedSection)
        if (selectedSectionKey && sectionsData[selectedSectionKey]) {
          setCurrentSectionHTML(sectionsData[selectedSectionKey])
        }
      } catch (error) {
        console.error('버전 데이터 로드 오류:', error)
      }
    }
    
    loadVersionData()
  }, [currentVersion, selectedSection])

  const findSectionById = (sections: DocumentSection[], id: string): DocumentSection | null => {
    for (const section of sections) {
      if (section.id === id) return section
      if (section.children) {
        const found = findSectionById(section.children, id)
        if (found) return found
      }
    }
    return null
  }

  const currentSection = findSectionById(mockDocumentData, selectedSection)

  const toggleLeftPanel = () => {
    setIsLeftPanelCollapsed(!isLeftPanelCollapsed)
  }

  const handleSectionModified = (sectionId: string, updatedHTML: string) => {
    setModifiedSections(prev => new Set([...prev, sectionId]))
    
    // 섹션 ID를 섹션 키로 변환
    const sectionKey = getSectionKeyFromId(sectionId)
    
    // 메모리 캐시 업데이트
    setVersionSectionsData(prev => ({
      ...prev,
      [sectionKey]: updatedHTML
    }))
    
    // 현재 보고 있는 섹션이라면 HTML도 업데이트
    if (sectionId === selectedSection) {
      setCurrentSectionHTML(updatedHTML)
    }
  }

  const handleCreateNewVersion = async () => {
    if (modifiedSections.size === 0) {
      alert('수정된 섹션이 없습니다.')
      return
    }
    
    setIsCreatingVersion(true)
    
    try {
      const description = prompt('새 버전에 대한 설명을 입력하세요:')
      
      // 수정된 섹션들의 데이터만 추출
      const modifiedSectionsData: Record<string, string> = {}
      modifiedSections.forEach(sectionId => {
        const sectionKey = getSectionKeyFromId(sectionId)
        if (versionSectionsData[sectionKey]) {
          modifiedSectionsData[sectionKey] = versionSectionsData[sectionKey]
        }
      })
      const state = await getProjectState()
      const sectionsData = await getVersionSections(state.currentVersion)

      // 바뀐 부분을 원본에 넣어서 새로운 데이터 생성 (최종 데이터)
      console.log("modifiedSections입니다.", modifiedSections)
      console.log("modifiedSectionsData입니다.", modifiedSectionsData)
      
      console.log("원본데이터입니다.", sectionsData)

      console.log("Type입니다", currentSection?.type)
      console.log("Name입니다", currentSection?.sectionName)

      
      const result = await createNewVersion(description || undefined, modifiedSectionsData)
      
      if (result.success) {
        // 상태 업데이트
        setCurrentVersion(result.version!)
        setModifiedSections(new Set())
        
        // 버전 목록 새로고침
        const versionList = await getVersionList()
        setVersions(versionList)
        
        alert(result.message)
      } else {
        alert(result.message)
      }
    } catch (error) {
      console.error('새 버전 생성 오류:', error)
      alert('새 버전 생성 중 오류가 발생했습니다.')
    } finally {
      setIsCreatingVersion(false)
    }
  }

  const handleSwitchVersion = async (version: string) => {
    if (version === currentVersion) return
    
    if (modifiedSections.size > 0) {
      const confirm = window.confirm('저장되지 않은 변경사항이 있습니다. 계속하시겠습니까?')
      if (!confirm) return
    }
    
    try {
      const result = await switchToVersion(version)
      
      if (result.success) {
        setCurrentVersion(version)
        setModifiedSections(new Set())
        
        // 새 버전의 섹션 데이터 로드
        const sectionsData = await getVersionSections(version)
        setVersionSectionsData(sectionsData)
        
        // 현재 선택된 섹션의 HTML 업데이트
        const selectedSectionKey = getSectionKeyFromId(selectedSection)
        if (selectedSectionKey && sectionsData[selectedSectionKey]) {
          setCurrentSectionHTML(sectionsData[selectedSectionKey])
        }
        
        alert(result.message)
      } else {
        alert(result.message)
      }
    } catch (error) {
      console.error('버전 전환 오류:', error)
      alert('버전 전환 중 오류가 발생했습니다.')
    }
  }

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault()
    setIsDragging(true)
    setStartX(e.clientX)
    setStartWidth(leftPanelWidth)
    
    // 드래그 중 텍스트 선택 방지
    document.body.style.userSelect = 'none'
    document.body.style.cursor = 'col-resize'
  }, [leftPanelWidth])

  const handleMouseMove = useCallback((e: MouseEvent) => {
    if (!isDragging || !containerRef.current) return
    
    const containerRect = containerRef.current.getBoundingClientRect()
    const deltaX = e.clientX - startX
    const containerWidth = containerRect.width
    const deltaPercent = (deltaX / containerWidth) * 100
    const newWidth = Math.max(15, Math.min(50, startWidth + deltaPercent))
    
    setLeftPanelWidth(newWidth)
  }, [isDragging, startX, startWidth])

  const handleMouseUp = useCallback(() => {
    if (isDragging) {
      setIsDragging(false)
      
      // 드래그 종료 후 스타일 복원
      document.body.style.userSelect = ''
      document.body.style.cursor = ''
    }
  }, [isDragging])

  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
      
      return () => {
        document.removeEventListener('mousemove', handleMouseMove)
        document.removeEventListener('mouseup', handleMouseUp)
      }
    }
  }, [isDragging, handleMouseMove, handleMouseUp])

  // 컴포넌트 언마운트 시 정리
  useEffect(() => {
    return () => {
      document.body.style.userSelect = ''
      document.body.style.cursor = ''
    }
  }, [])

  return (
    <div ref={containerRef} className="h-screen flex flex-col bg-white">
      {/* Header */}
      <div className="bg-blue-600 text-white shadow-sm">
        <div className="px-6 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <h1 className="text-xl font-bold">Keommang</h1>
              <div className="h-5 w-px bg-blue-400"></div>
              <div className="flex items-center space-x-3">
                <span className="bg-orange-500 px-2 py-1 rounded text-xs font-medium">코스닥</span>
                <span className="font-medium">오픈엣지테크놀로지</span>
                
                {/* 버전 선택 드롭다운 */}
                <VersionSelector
                  currentVersion={currentVersion}
                  versions={versions}
                  onVersionSelect={handleSwitchVersion}
                  disabled={isCreatingVersion}
                />
              </div>
            </div>
            <div className="flex items-center space-x-3">
              {/* 최종 저장 버튼 */}
              {modifiedSections.size > 0 && (
                <Button
                  onClick={handleCreateNewVersion}
                  disabled={isCreatingVersion}
                  size="sm"
                  variant="outline"
                  className="bg-green-600 text-white hover:bg-green-700 border-green-600"
                >
                  <Plus className="w-4 h-4 mr-1" />
                  {isCreatingVersion ? '생성 중...' : '최종 저장'}
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Warning Banner */}
      <div className="bg-yellow-100 border-l-4 border-yellow-500 p-2 text-sm text-yellow-700">
        본 문서는 AI가 작성한 초안이므로, 제출 전 반드시 검토하시기 바랍니다.
        {modifiedSections.size > 0 && (
          <span className="ml-4 font-medium text-orange-600">
            ({modifiedSections.size}개 섹션이 수정됨)
          </span>
        )}
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden relative">
        {/* Left Panel - Table of Contents */}
        <div 
          className={`bg-gray-50 border-r transition-all duration-200 ease-in-out ${
            isLeftPanelCollapsed ? 'w-0' : ''
          }`}
          style={{ 
            width: isLeftPanelCollapsed ? '0%' : `${leftPanelWidth}%`,
            minWidth: isLeftPanelCollapsed ? '0px' : '200px'
          }}
        >
          {!isLeftPanelCollapsed && (
            <div className="h-full flex flex-col">
              <div className="bg-blue-100 dark:bg-blue-900 p-3 border-b border-blue-300 dark:border-blue-700 text-center">
                <h3 className="font-semibold text-blue-800 dark:text-blue-100">📑 문서 목차</h3>
              </div>
              <div className="flex-1 overflow-auto">
                <TableOfContents
                  sections={mockDocumentData}
                  selectedSection={selectedSection}
                  onSectionSelect={setSelectedSection}
                  expandedSections={expandedSections}
                  setExpandedSections={setExpandedSections}
                  modifiedSections={modifiedSections}
                />
              </div>
            </div>
          )}
        </div>

        {/* Divider */}
        {!isLeftPanelCollapsed && (
          <div
            className={`w-1 bg-gray-300 hover:bg-blue-400 transition-colors cursor-col-resize select-none ${
              isDragging ? 'bg-blue-500' : ''
            }`}
            onMouseDown={handleMouseDown}
          >
            <div className="w-full h-full flex items-center justify-center">
              <div className="w-0.5 h-8 bg-gray-400 rounded-full opacity-60"></div>
            </div>
          </div>
        )}

        {/* Toggle Button */}
        <Button
          variant="outline"
          size="sm"
          className={`absolute top-1/2 z-10 transform -translate-y-1/2 transition-all duration-200 ${
            isLeftPanelCollapsed ? 'left-2' : ''
          }`}
          style={{ 
            left: isLeftPanelCollapsed ? '8px' : `calc(${leftPanelWidth}% + 4px)`,
            transition: 'left 0.2s ease-in-out'
          }}
          onClick={toggleLeftPanel}
        >
          {isLeftPanelCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </Button>

        {/* Right Panel - Document Content */}
        <div className="flex-1 bg-white overflow-hidden">
          {isLoadingSection ? (
            <div className="flex items-center justify-center h-full">
              <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
              <span className="ml-2 text-gray-600">섹션을 불러오는 중...</span>
            </div>
          ) : (
            <DocumentContent 
              htmlContent={currentSectionHTML}
              sectionId={selectedSection}
              sectionName={currentSection?.sectionName}
              sectionType={currentSection?.type}
              onSectionModified={handleSectionModified}
            />
          )}
        </div>
      </div>
    </div>
  )
}