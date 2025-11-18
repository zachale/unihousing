import { NotificationDialog } from "./notification-dialog"

interface UnsupportedSchoolDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  schoolName: string
  onSubmit: (email: string) => void
}

/**
 * Dialog for notifying users when their school is not yet supported.
 * This is a convenience wrapper around the reusable NotificationDialog.
 */
export function UnsupportedSchoolDialog({
  open,
  onOpenChange,
  schoolName,
  onSubmit,
}: UnsupportedSchoolDialogProps) {
  return (
    <NotificationDialog
      open={open}
      onOpenChange={onOpenChange}
      title="We don't support your school yet!"
      description="We'll notify you when your school is added to our platform."
      onSubmit={onSubmit}
    />
  )
}

