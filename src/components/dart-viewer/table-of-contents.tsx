'use client'

import { ChevronDown, ChevronRight, Edit } from 'lucide-react'

interface DocumentSection {
  id: string
  title: string
  children?: DocumentSection[]
}

interface TableOfContentsProps {
  sections: DocumentSection[]
  selectedSection: string
  onSectionSelect: (id: string) => void
  expandedSections: Set<string>
  setExpandedSections: (sections: Set<string>) => void
  modifiedSections: Set<string>
  level?: number
}

export function TableOfContents({ 
  sections, 
  selectedSection, 
  onSectionSelect,
  expandedSections,
  setExpandedSections,
  modifiedSections,
  level = 0 
}: TableOfContentsProps) {

  const toggleExpanded = (id: string) => {
    const newExpanded = new Set(expandedSections)
    if (newExpanded.has(id)) {
      newExpanded.delete(id)
    } else {
      newExpanded.add(id)
    }
    setExpandedSections(newExpanded)
  }

  return (
    <ul className={`${level === 0 ? '' : 'ml-4'}`}>
      {sections.map((section) => (
        <li key={section.id} className="mb-1">
          <div className="flex items-center">
            {section.children && section.children.length > 0 && (
              <button
                onClick={() => toggleExpanded(section.id)}
                className="p-1 hover:bg-gray-200 rounded"
              >
                {expandedSections.has(section.id) ? (
                  <ChevronDown className="w-3 h-3" />
                ) : (
                  <ChevronRight className="w-3 h-3" />
                )}
              </button>
            )}
            {(!section.children || section.children.length === 0) && (
              <div className="w-5" />
            )}
            <button
              onClick={() => onSectionSelect(section.id)}
              className={`flex-1 text-left p-2 text-sm hover:bg-blue-50 rounded transition-colors flex items-center justify-between ${
                selectedSection === section.id 
                  ? 'bg-blue-100 text-blue-700 font-medium' 
                  : 'text-gray-700'
              }`}
            >
              <span className="flex-1">{section.title}</span>
              {modifiedSections.has(section.id) && (
                <div className="flex items-center gap-1 ml-2">
                  <Edit className="w-3 h-3 text-orange-500" />
                  <span className="text-xs text-orange-600 font-medium">수정됨</span>
                </div>
              )}
            </button>
          </div>
          
          {section.children && 
           section.children.length > 0 && 
           expandedSections.has(section.id) && (
            <TableOfContents
              sections={section.children}
              selectedSection={selectedSection}
              onSectionSelect={onSectionSelect}
              expandedSections={expandedSections}
              setExpandedSections={setExpandedSections}
              modifiedSections={modifiedSections}
              level={level + 1}
            />
          )}
        </li>
      ))}
    </ul>
  )
}
