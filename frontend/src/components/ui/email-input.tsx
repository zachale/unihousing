import * as React from "react"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import { isValidEmail } from "@/lib/validation"
import { useEmailValidation } from "@/hooks/use-email-validation"

interface EmailInputProps extends Omit<React.ComponentProps<typeof Input>, "type" | "value" | "onChange" | "onBlur"> {
  value?: string
  onValueChange?: (value: string) => void
  onValidationChange?: (isValid: boolean) => void
  errorMessage?: string
  validateOnMount?: boolean
  resetOnClose?: boolean
  isOpen?: boolean
}

export function EmailInput({
  value: controlledValue,
  onValueChange,
  onValidationChange,
  errorMessage: customErrorMessage,
  validateOnMount = false,
  resetOnClose = false,
  isOpen,
  className,
  onKeyDown,
  ...props
}: EmailInputProps) {
  const isControlled = controlledValue !== undefined
  const [isTouched, setIsTouched] = React.useState(validateOnMount)
  
  // Use controlled value or hook's internal state
  const {
    email: internalEmail,
    isValid: hookIsValid,
    showError: hookShowError,
    errorMessage: internalErrorMessage,
    handleBlur: hookHandleBlur,
    handleChange: internalHandleChange,
  } = useEmailValidation({
    initialValue: "",
    validateOnMount,
    resetOnClose: false, // We'll handle reset manually for controlled
    isOpen: undefined, // Don't auto-reset for controlled
  })

  const currentEmail = isControlled ? (controlledValue || "") : internalEmail
  const isValid = currentEmail === "" || isValidEmail(currentEmail)
  const showError = isTouched && !isValid
  const errorMessage = customErrorMessage || internalErrorMessage

  // Reset touched state when dialog closes (for controlled mode)
  React.useEffect(() => {
    if (resetOnClose && isOpen === false && isControlled) {
      setIsTouched(validateOnMount)
    }
  }, [isOpen, resetOnClose, isControlled, validateOnMount])

  // Notify parent of validation changes
  React.useEffect(() => {
    onValidationChange?.(isValid)
  }, [isValid, onValidationChange])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value
    if (!isControlled) {
      internalHandleChange(e)
    }
    onValueChange?.(newValue)
  }

  const handleBlur = () => {
    setIsTouched(true)
    if (!isControlled) {
      hookHandleBlur()
    }
  }

  return (
    <div className="grid gap-2">
      <Input
        type="email"
        value={currentEmail}
        onChange={handleChange}
        onBlur={handleBlur}
        onKeyDown={onKeyDown}
        className={cn(showError && "border-destructive", className)}
        {...props}
      />
      {showError && errorMessage && (
        <p className="text-sm text-destructive">{errorMessage}</p>
      )}
    </div>
  )
}

