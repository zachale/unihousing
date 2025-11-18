import { useState, useCallback } from "react"
import { type SchoolOption } from "./types"

interface UseSchoolSelectionOptions {
  onUnsupportedSchoolSelected?: (schoolName: string, email: string) => void
}

export function useSchoolSelection(options?: UseSchoolSelectionOptions) {
  const [selectedValue, setSelectedValue] = useState<string>("")
  const [dialogOpen, setDialogOpen] = useState(false)
  const [requestedSchool, setRequestedSchool] = useState<string>("")

  const handleValueChange = useCallback((value: string) => {
    setSelectedValue(value)
  }, [])

  const handleSend = useCallback(
    (schools: SchoolOption[]) => {
      if (!selectedValue) return

      const selectedSchool = schools.find((school) => school.value === selectedValue)
      if (selectedSchool && !selectedSchool.supported) {
        setRequestedSchool(selectedSchool.label)
        setDialogOpen(true)
      }
    },
    [selectedValue]
  )

  const handleSubmitNotification = useCallback(
    (email: string) => {
      if (options?.onUnsupportedSchoolSelected) {
        options.onUnsupportedSchoolSelected(requestedSchool, email)
      }
      setDialogOpen(false)
    },
    [requestedSchool, options]
  )

  return {
    selectedValue,
    dialogOpen,
    requestedSchool,
    setDialogOpen,
    handleValueChange,
    handleSend,
    handleSubmitNotification,
  }
}

