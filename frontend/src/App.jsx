import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";

import ImageRagPage
  from "./pages/ImageRagPage";


function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route
              path="/"
              element={
                <ImageRagPage />
              }
          />
        </Routes>
      </BrowserRouter>
  );
}


export default App;