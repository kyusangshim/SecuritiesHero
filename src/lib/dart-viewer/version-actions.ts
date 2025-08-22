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
    modifiedSections: string[]; // 배열 또는 null
  };
}

// DB에서 모든 버전 데이터 가져오기
export async function fetchVersionsFromDB(userId: number): Promise<DBVersionData> {
  try {
    const response = await fetch(`http://localhost:8081/api/versions?userId=${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store' // 항상 최신 데이터 가져오기
    });
    
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

// 프로젝트 초기화 (DB 기반)
export async function initializeProject(userId: number) {
  try {
    const versionsData = await fetchVersionsFromDB(userId)

    // v0가 존재하는지 확인
    if (versionsData.v0) {
      return versionsData
    }

    const initialData = await initializeData()

    const response = await fetch('http://localhost:8081/api/versions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        version: 'v0',
        version_number: 0,
        description: '초기 버전',
        sectionsData: initialData || {},
        createdAt: new Date().toISOString()
      })
    })

    const result = await response.json()

    const initVersion: DBVersionData = {
      v0: {
        createdAt: result.createdAt,
        description: result.description,
        modifiedSections: [],
        section1: result.section1,
        section2: result.section2,
        section3: result.section3,
        section4: result.section4,
        section5: result.section5,
        section6: result.section6,
      }
    }

    return initVersion
  } catch (error) {
    console.error('프로젝트 초기화 오류:', error)
    return {}
  }
}


// 통합된 프로젝트 상태 초기화 + 로드
export async function loadFullProjectState(userId: number): Promise<ProjectState & { sectionsData: Record<string, string> }> {
  try {

    // 1️⃣ 먼저 프로젝트 초기화
    const versionsData = await initializeProject(userId)
    const versionKeys = Object.keys(versionsData)
    
    if (!versionsData || versionKeys.length === 0) {
      throw new Error("프로젝트 초기화 실패")
    }

    // 3️⃣ 현재 버전 결정
    let currentVersion = 'v0'
    if (versionKeys.includes('editing')) {
      currentVersion = 'editing'
    } else if (versionKeys.length > 0) {
      const numericVersions = versionKeys.filter(v => v.startsWith('v'))
      numericVersions.sort((a, b) => {
        const aNum = parseInt(a.replace('v', ''))
        const bNum = parseInt(b.replace('v', ''))
        return aNum - bNum
      })
      currentVersion = numericVersions[numericVersions.length - 1]
    }

    // 4️⃣ 버전 목록 생성
    const versions: VersionInfo[] = versionKeys.map(version => ({
      version,
      createdAt: versionsData[version].createdAt,
      description: versionsData[version].description || `버전 ${version}`,
      modifiedSections: versionsData[version].modifiedSections || []
    }))

    const editingModifiedSections = versionsData['editing']?.modifiedSections

    let parseModif: string[] = []
    if (typeof editingModifiedSections == "string"){
      parseModif = JSON.parse(editingModifiedSections)
    }

    
    // 5️⃣ 수정된 섹션 추출
    const modifiedSections = new Set(
      currentVersion === 'editing'
        ? parseModif || []
        : []
    )

    // 6️⃣ 섹션 데이터 가져오기
    const versionData = versionsData[currentVersion] || {}
    const sectionsData: Record<string, string> = {}
    Object.keys(versionData).forEach(key => {
      if (key.startsWith("section")) {
        sectionsData[key] = versionData[key as keyof typeof versionData] as string || ""
      }
    })


    return {
      currentVersion,
      versions,
      modifiedSections,
      sectionsData
    }
  } catch (error) {
    console.error('loadFullProjectState 오류:', error)
    return {
      currentVersion: 'v0',
      versions: [],
      modifiedSections: new Set(),
      sectionsData: {}
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
export async function createNewVersion(userId: number, description?: string) {
  try {
    // DB에 새 버전 저장 API 호출
    const response = await fetch('http://localhost:8081/api/versions/finalize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        description: description || `설명 없음`,
        createdAt: new Date().toISOString()
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const result = await response.json()
    
    return { 
      success: true, 
      message: result.message,
      version: result.new_version 
    }
  } catch (error) {
    console.error('새 버전 생성 오류:', error)
    return { success: false, message: '새 버전 생성 중 오류가 발생했습니다.' }
  }
}


// 특정 버전의 모든 섹션 데이터 가져오기
export async function getVersionSections(version: string, userId: number): Promise<Record<string, string>> {
  try {
    const versionsData = await fetchVersionsFromDB(userId)
    
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
    }
  } catch (error) {
    console.error('버전 섹션 데이터 가져오기 오류:', error)
    return {}
  }
}