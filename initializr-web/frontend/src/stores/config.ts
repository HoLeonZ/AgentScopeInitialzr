// initializr-web/frontend/src/stores/config.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ProjectRequest } from '@/types'
import { api } from '@/api'

export const useConfigStore = defineStore('config', () => {
  // Form state
  const form = ref<ProjectRequest>({
    name: '',
    description: '',
    author: '',
    agent_type: 'basic',
    python_version: '3.14',
    model_provider: 'dashscope',
    model_settings: {},
    enable_memory: false,
    short_term_memory: null,
    long_term_memory: null,
    enable_knowledge: false,
    knowledge_config: null,
    enable_tools: false,
    tools: [],
    enable_skills: false,
    skills: [],
    enable_hooks: false,
    hooks: [],
    enable_formatter: false,
    formatter: null,
    enable_pipeline: false,
    pipeline_config: null,
    generate_tests: false,
    generate_evaluation: false,
    evaluator_type: 'general',
    enable_openjudge: false,
    openjudge_graders: [],
    initial_benchmark_tasks: 0,
  })

  // Loading state
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Current step in multi-step form
  const currentStep = ref(1)
  const totalSteps = 4

  // Computed
  const isValid = computed(() => {
    return form.value.name.trim().length > 0
  })

  // Actions
  const setField = <K extends keyof ProjectRequest>(field: K, value: ProjectRequest[K]) => {
    form.value[field] = value
  }

  const resetForm = () => {
    form.value = {
      name: '',
      description: '',
      author: '',
      agent_type: 'basic',
      python_version: '3.14',
      model_provider: 'dashscope',
      model_settings: {},
      enable_memory: false,
      short_term_memory: null,
      long_term_memory: null,
      enable_knowledge: false,
      knowledge_config: null,
      enable_tools: false,
      tools: [],
      enable_skills: false,
      skills: [],
      enable_hooks: false,
      hooks: [],
      enable_formatter: false,
      formatter: null,
      enable_pipeline: false,
      pipeline_config: null,
      generate_tests: false,
      generate_evaluation: false,
      evaluator_type: 'general',
      enable_openjudge: false,
      openjudge_graders: [],
      initial_benchmark_tasks: 0,
    }
    currentStep.value = 1
    error.value = null
  }

  const nextStep = () => {
    if (currentStep.value < totalSteps) {
      currentStep.value++
    }
  }

  const prevStep = () => {
    if (currentStep.value > 1) {
      currentStep.value--
    }
  }

  const setCurrentStep = (step: number) => {
    if (step >= 1 && step <= totalSteps) {
      currentStep.value = step
    }
  }

  const generateProject = async () => {
    if (!isValid.value) {
      error.value = 'Project name is required'
      return null
    }

    loading.value = true
    error.value = null

    try {
      const response = await api.generateProject(form.value)
      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to generate project'
      return null
    } finally {
      loading.value = false
    }
  }

  return {
    form,
    loading,
    error,
    currentStep,
    totalSteps,
    isValid,
    setField,
    resetForm,
    setCurrentStep,
    nextStep,
    prevStep,
    generateProject,
  }
})
