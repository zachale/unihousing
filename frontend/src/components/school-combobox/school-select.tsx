import * as React from "react"
import { Check, ChevronsUpDown } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { type SchoolOption } from "./types"

interface SchoolSelectProps {
  options: SchoolOption[]
  value?: string
  onValueChange: (value: string) => void
  placeholder?: string
  searchPlaceholder?: string
  emptyMessage?: string
  className?: string
  popoverClassName?: string
}

export function SchoolSelect({
  options,
  value,
  onValueChange,
  placeholder = "Select a school...",
  searchPlaceholder = "Search school...",
  emptyMessage = "No school found.",
  className,
  popoverClassName,
}: SchoolSelectProps) {
  const [open, setOpen] = React.useState(false)

  const selectedSchool = options.find((school) => school.value === value)

  const handleSelect = (selectedValue: string) => {
    onValueChange(selectedValue === value ? "" : selectedValue)
    setOpen(false)
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          type="button"
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className={cn("w-[400px] justify-between", className)}
        >
          {selectedSchool?.label || placeholder}
          <ChevronsUpDown className="opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className={cn("w-[400px] p-0", popoverClassName)} align="start">
        <Command className="rounded-lg border shadow-md">
          <CommandInput placeholder={searchPlaceholder} />
          <CommandList>
            <CommandEmpty>{emptyMessage}</CommandEmpty>
            <CommandGroup>
              {options.map((school) => (
                <CommandItem
                  key={school.value}
                  value={school.value}
                  onSelect={handleSelect}
                >
                  {school.label}
                  <Check
                    className={cn(
                      "ml-auto",
                      value === school.value ? "opacity-100" : "opacity-0"
                    )}
                  />
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}

