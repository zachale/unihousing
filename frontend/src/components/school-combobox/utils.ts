import { type School, type SchoolOption } from "./types"

export function transformSchoolsToOptions(schools: School[]): SchoolOption[] {
  return schools.map((school) => ({
    value: school.value,
    label: school.label,
    supported: school.supported,
  }))
}

