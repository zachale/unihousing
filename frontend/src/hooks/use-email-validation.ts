import { useState, useEffect, useCallback } from "react"
import { isValidEmail } from "@/lib/validation"

interface UseEmailValidationOptions {
  initialValue?: string
  validateOnMount?: boolean
  resetOnClose?: boolean
  isOpen?: boolean
}

interface UseEmailValidationReturn {
  email: string
  setEmail: (email: string) => void
  isValid: boolean
  isTouched: boolean
  showError: boolean
  errorMessage: string
  handleBlur: () => void
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  reset: () => void
  validate: () => boolean
}

export function useEmailValidation(
  options: UseEmailValidationOptions = {}
): UseEmailValidationReturn {
  const {
    initialValue = "",
    validateOnMount = false,
    resetOnClose = false,
    isOpen,
  } = options

  const [email, setEmail] = useState(initialValue)
  const [isTouched, setIsTouched] = useState(validateOnMount)

  const isValid = email === "" || isValidEmail(email)
  const showError = isTouched && !isValid
  const errorMessage = showError ? "Please enter a valid email address" : ""

  // Reset when dialog/form closes if enabled
  useEffect(() => {
    if (resetOnClose && isOpen === false) {
      reset()
    }
  }, [isOpen, resetOnClose])

  const handleBlur = useCallback(() => {
    setIsTouched(true)
  }, [])

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value)
  }, [])

  const reset = useCallback(() => {
    setEmail(initialValue)
    setIsTouched(validateOnMount)
  }, [initialValue, validateOnMount])

  const validate = useCallback(() => {
    setIsTouched(true)
    return isValidEmail(email)
  }, [email])

  return {
    email,
    setEmail,
    isValid,
    isTouched,
    showError,
    errorMessage,
    handleBlur,
    handleChange,
    reset,
    validate,
  }
}

