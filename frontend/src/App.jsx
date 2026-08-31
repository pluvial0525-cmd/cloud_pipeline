import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import ImageRagPage from "./pages/ImageRagPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";


function App() {

    const token = localStorage.getItem(
        "access_token",
    );


    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path="/login"
                    element={
                        token
                            ? (
                                <Navigate
                                    to="/"
                                    replace
                                />
                            )
                            : (
                                <LoginPage />
                            )
                    }
                />

                <Route
                    path="/signup"
                    element={
                        token
                            ? (
                                <Navigate
                                    to="/"
                                    replace
                                />
                            )
                            : (
                                <SignupPage />
                            )
                    }
                />

                <Route
                    path="/"
                    element={
                        token
                            ? (
                                <ImageRagPage />
                            )
                            : (
                                <Navigate
                                    to="/login"
                                    replace
                                />
                            )
                    }
                />
            </Routes>
        </BrowserRouter>
    );

}


export default App;