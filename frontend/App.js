import React from "react";

const App = () => {
    return (
      <>
        <Header />
        <main className="py-3">
          <Container>
            <Outlet />
          </Container>
        </main>
        <Footer />
        <ToastContainer />
      </>
    )
  }
  
  export default App