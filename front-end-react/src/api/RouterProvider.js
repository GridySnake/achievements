// import {createContext, useContext, useEffect, useState} from "react";
// import {useLocation} from "react-router-dom";
//
// const RouterContext = createContext();
//
// const RouterProvider = ({children}) => {
//     const location = useLocation()
//     const [currentPath, setCurrentPath] = useState(location.pathname);
//     const [previousPath, setPreviousPath] = useState();
//
//   useEffect(() => {
//     if (location.pathname !== currentPath) {
//       setPreviousPath(currentPath);
//       setCurrentPath(location.pathname);
//     }
//   }, [location.pathname]);
//     return <RouterContext.Provider value={{from: previousPath, to: currentPath}}>
//         {children}
//       </RouterContext.Provider>
//     };
//
// const useRouterContext = () => {
//     return useContext(RouterContext)
// };
//
// export {RouterProvider, useRouterContext};