'use server'

import { initializeData } from "../../data/dart-viewer/initializeData"

export interface VersionInfo {
  version: string
  createdAt: string
  description?: string
  modifiedSections: string[]
}

export interface ProjectState {
  currentVersion: string
  versions: VersionInfo[]
  modifiedSections: Set<string>
}

export interface DBVersionData {
  [version: string]: {
    section1: string;
    section2: string;
    section3: string;
    section4: string;
    section5: string;
    section6: string;
    description: string;
    createdAt: string;
  }
}

// DB에서 모든 버전 데이터 가져오기
export async function fetchVersionsFromDB(): Promise<DBVersionData> {
  try {
    const response = await fetch('http://localhost:8000/versions', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store' // 항상 최신 데이터 가져오기
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('DB에서 버전 데이터 가져오기 오류:', error)
    throw error
  }
}

// 특정 버전의 특정 섹션 HTML 가져오기
export async function getSectionHTML(version: string, sectionKey: string): Promise<string> {
  try {
    const versionsData = await fetchVersionsFromDB()
    
    if (!versionsData[version]) {
      throw new Error(`버전 ${version}을 찾을 수 없습니다.`)
    }
    
    const htmlContent = versionsData[version][sectionKey as keyof typeof versionsData[typeof version]]
    
    if (!htmlContent) {
      console.warn(`섹션 ${sectionKey}의 HTML 내용이 비어있습니다.`)
      return ''
    }
    
    return htmlContent
  } catch (error) {
    console.error('섹션 HTML 가져오기 오류:', error)
    return ''
  }
}

// 프로젝트 초기화 (DB 기반)
export async function initializeProject() {
  try {
    const versionsData = await fetchVersionsFromDB()
    
    // v0가 존재하는지 확인
    if (versionsData.v0) {
      return { success: true, message: '프로젝트가 이미 초기화되어 있습니다.', version: 'v0' }
    }
    
    const initialData = initializeData();

    
    const response = await fetch('http://localhost:8000/versions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: 1,
        version: "v0",
        description: "초기 버전",
        sectionsData: initialData || {}, // 수정된 섹션들의 HTML 데이터
        createdAt: new Date().toISOString()
      })
    })
    
    return { success: true, message: 'v0 초기 템플릿이 생성되었습니다.', version: 'v0' }
  } catch (error) {
    console.error('프로젝트 초기화 오류:', error)
    return { success: false, message: '프로젝트 초기화 중 오류가 발생했습니다.' }
  }
}

// 현재 프로젝트 상태 가져오기 (DB 기반)
export async function getProjectState(): Promise<ProjectState> {
  try {
    const versionsData = await fetchVersionsFromDB()
    const versionKeys = Object.keys(versionsData).sort((a, b) => {
      const aNum = parseInt(a.replace('v', ''))
      const bNum = parseInt(b.replace('v', ''))
      return aNum - bNum
    })
    
    // 버전 정보 생성
    const versions: VersionInfo[] = versionKeys.map(version => ({
      version,
      createdAt: versionsData[version].createdAt, // DB에 createdAt이 없다면 임시값 ( new Date().toISOString() )
      description: versionsData[version].description || `버전 ${version}`,
      modifiedSections: [] // 현재 수정 상태는 클라이언트에서 관리
    }))
    
    // 가장 최신 버전을 현재 버전으로 설정
    const currentVersion = versionKeys[versionKeys.length - 1] || 'v0'
    
    return {
      currentVersion,
      versions,
      modifiedSections: new Set() // 초기에는 수정된 섹션 없음
    }
  } catch (error) {
    console.error('프로젝트 상태 로드 오류:', error)
    // 기본 상태 반환
    return {
      currentVersion: 'v0',
      versions: [],
      modifiedSections: new Set()
    }
  }
}

// 섹션 수정 상태 업데이트 (클라이언트 메모리에서만 관리)
export async function markSectionAsModified(sectionId: string) {
  // DB 기반에서는 실제로 저장하지 않고, 클라이언트 상태로만 관리
  // 실제 저장은 createNewVersion에서만 발생
  return { success: true, message: '섹션이 수정됨으로 표시되었습니다.' }
}

// 새 버전 생성 (DB에 저장)
export async function createNewVersion(description?: string, sectionsData?: Record<string, string>) {
  try {
    const versionsData = await fetchVersionsFromDB()
    const versionKeys = Object.keys(versionsData)
    
    // 새 버전 번호 계산
    const versionNumbers = versionKeys
      .map(v => parseInt(v.replace('v', '')))
      .filter(n => !isNaN(n))
    
    const maxVersion = Math.max(...versionNumbers, -1)
    const newVersionNum = maxVersion + 1
    const newVersion = `v${newVersionNum}`
    
    // DB에 새 버전 저장 API 호출
    const response = await fetch('http://localhost:8000/versions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: 1,
        version: newVersion,
        description: description || `버전 ${newVersion}`,
        sectionsData: sectionsData || {}, // 수정된 섹션들의 HTML 데이터
        createdAt: new Date().toISOString()
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const result = await response.json()
    
    return { 
      success: true, 
      message: `${newVersion} 버전이 생성되었습니다.`,
      version: newVersion 
    }
  } catch (error) {
    console.error('새 버전 생성 오류:', error)
    return { success: false, message: '새 버전 생성 중 오류가 발생했습니다.' }
  }
}

// 특정 버전으로 전환 (DB에서 해당 버전 데이터 로드)
export async function switchToVersion(targetVersion: string) {
  try {
    const versionsData = await fetchVersionsFromDB()
    
    if (!versionsData[targetVersion]) {
      return { success: false, message: '해당 버전을 찾을 수 없습니다.' }
    }
    
    // DB 기반에서는 실제 파일 복사가 아닌 버전 전환만 표시
    return { 
      success: true, 
      message: `${targetVersion}으로 전환되었습니다.`,
      version: targetVersion 
    }
  } catch (error) {
    console.error('버전 전환 오류:', error)
    return { success: false, message: '버전 전환 중 오류가 발생했습니다.' }
  }
}

// 버전 목록 가져오기
export async function getVersionList(): Promise<VersionInfo[]> {
  try {
    const state = await getProjectState()
    return state.versions
  } catch (error) {
    console.error('버전 목록 로드 오류:', error)
    return []
  }
}

// 특정 버전의 모든 섹션 데이터 가져오기
export async function getVersionSections(version: string): Promise<Record<string, string>> {
  try {
    const versionsData = await fetchVersionsFromDB()
    
    if (!versionsData[version]) {
      throw new Error(`버전 ${version}을 찾을 수 없습니다.`)
    }
    
    const versionData = versionsData[version]
    
    return {
      'section1': versionData.section1 || '',
      'section2': versionData.section2 || '',
      'section3': versionData.section3 || '',
      'section4': versionData.section4 || '',
      'section5': versionData.section5 || '',
      'section6': versionData.section6 || '',
      // 추가 섹션들...
    }
  } catch (error) {
    console.error('버전 섹션 데이터 가져오기 오류:', error)
    return {}
  }
}

// 섹션 데이터 업데이트 (DB에 저장)
export async function updateSectionInDB(version: string, sectionKey: string, htmlContent: string) {
  try {
    const response = await fetch(`http://localhost:8000/versions/${version}/sections/${sectionKey}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        htmlContent
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return { success: true, message: '섹션이 업데이트되었습니다.' }
  } catch (error) {
    console.error('섹션 업데이트 오류:', error)
    return { success: false, message: '섹션 업데이트 중 오류가 발생했습니다.' }
  }
}