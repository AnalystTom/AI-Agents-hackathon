import React from 'react'

export default function Footer() {

    const year = new Date().getFullYear()
  return (
    <footer>
        <div className="container">
            <div className="row">
                <div className="col">
                    <p className="text-light text-center mt-0 my-2">
                        &copy; {year} | All rights reserved
                    </p>
                </div>
            </div>
        </div>
    </footer>
  )
}
