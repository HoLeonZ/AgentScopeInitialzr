// initializr-web/frontend/src/api/index.ts
import apiClient from './client'
import type {
  ProjectRequest,
  ProjectResponse,
  TemplatesResponse,
  ModelsResponse,
  ExtensionsResponse,
  HealthResponse,
  DetailedHealthResponse,
} from '@/types'

export const api = {
  // Health checks
  getHealth: async (): Promise<HealthResponse> => {
    const response = await apiClient.get<HealthResponse>('/../health')
    return response.data
  },

  getDetailedHealth: async (): Promise<DetailedHealthResponse> => {
    const response = await apiClient.get<DetailedHealthResponse>('/../health/detailed')
    return response.data
  },

  // Metadata
  getTemplates: async (): Promise<TemplatesResponse> => {
    const response = await apiClient.get<TemplatesResponse>('/templates')
    return response.data
  },

  getModels: async (): Promise<ModelsResponse> => {
    const response = await apiClient.get<ModelsResponse>('/models')
    return response.data
  },

  getExtensions: async (): Promise<ExtensionsResponse> => {
    const response = await apiClient.get<ExtensionsResponse>('/extensions')
    return response.data
  },

  // Project generation
  generateProject: async (request: ProjectRequest): Promise<ProjectResponse> => {
    const response = await apiClient.post<ProjectResponse>('/projects/generate', request)
    return response.data
  },

  getDownloadUrl: (projectId: string): string => {
    return `/api/v1/projects/download/${projectId}`
  },
}
