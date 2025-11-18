import { Send } from "lucide-react"
import { Button } from "@/components/ui/button"
import { SchoolSelect } from "./school-select"
import { UnsupportedSchoolDialog } from "./unsupported-school-dialog"
import { useSchoolSelection } from "./use-school-selection"
import { transformSchoolsToOptions } from "./utils"
import universities from "./schools"

const schoolOptions = transformSchoolsToOptions(universities)

export function SchoolCombobox() {
  const {
    selectedValue,
    dialogOpen,
    requestedSchool,
    setDialogOpen,
    handleValueChange,
    handleSend,
    handleSubmitNotification,
  } = useSchoolSelection({
    onUnsupportedSchoolSelected: (schoolName, email) => {
      // TODO: Send email request to backend
      console.log(`Requesting school: ${schoolName}, email: ${email}`)
    },
  })

  return (
    <div className="flex items-center justify-center gap-2">
      <SchoolSelect
        options={schoolOptions}
        value={selectedValue}
        onValueChange={handleValueChange}
        placeholder="Search your school..."
      />
      <Button
        type="button"
        variant="default"
        size="icon"
        aria-label="Send"
        onClick={() => handleSend(schoolOptions)}
      >
        <Send className="h-4 w-4" />
      </Button>

      <UnsupportedSchoolDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        schoolName={requestedSchool}
        onSubmit={handleSubmitNotification}
      />
    </div>
  )
}
