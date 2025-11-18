import * as React from "react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { EmailInput } from "@/components/ui/email-input"
import { isValidEmail } from "@/lib/validation"

interface NotificationDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  title: string
  description: string
  submitLabel?: string
  cancelLabel?: string
  emailPlaceholder?: string
  onSubmit: (email: string) => void
}

export function NotificationDialog({
  open,
  onOpenChange,
  title,
  description,
  submitLabel = "Notify Me",
  cancelLabel = "Cancel",
  emailPlaceholder = "your.email@example.com",
  onSubmit,
}: NotificationDialogProps) {
  const [email, setEmail] = React.useState("")
  const [isValid, setIsValid] = React.useState(false)

  const handleSubmit = () => {
    if (email && isValidEmail(email)) {
      onSubmit(email)
      setEmail("")
      onOpenChange(false)
    }
  }

  const handleCancel = () => {
    setEmail("")
    onOpenChange(false)
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && email && isValidEmail(email)) {
      handleSubmit()
    }
  }

  // Reset when dialog closes
  React.useEffect(() => {
    if (!open) {
      setEmail("")
      setIsValid(false)
    }
  }, [open])

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <EmailInput
            value={email}
            onValueChange={setEmail}
            onValidationChange={setIsValid}
            placeholder={emailPlaceholder}
            onKeyDown={handleKeyDown}
            resetOnClose
            isOpen={open}
          />
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={handleCancel}>
            {cancelLabel}
          </Button>
          <Button onClick={handleSubmit} disabled={!email || !isValid}>
            {submitLabel}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

