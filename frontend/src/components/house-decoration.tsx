import houseSvg from '@/assets/house.svg'

export function HouseDecoration() {
  return (
    <div className="house-decoration">
      <img 
        src={houseSvg} 
        alt="House decoration" 
        className="house-svg"
      />
    </div>
  )
}

