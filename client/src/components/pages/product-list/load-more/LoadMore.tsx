// import type { ReactElement } from 'react';

// export const LoadMore = (): ReactElement => {
//     const [page, setPage] = useState<number>(1);
//     const [loadMoreDisabled, setLoadMoreDisabled] = useState<boolean>(false);
//     const resetPage = () => {
//         setPage(() => 1);
//     };

//     const loadMoreHandler = (): void => {
//         if (count <= products.length) {
//             setLoadMoreDisabled(true);

//             return;
//         }

//         setPage(() => page + 1);
//     };

//     useEffect(() => {
//         resetPage();
//         setLoadMoreDisabled(false);
//     }, [categoryName]);

//     useEffect(() => {
//         if (products.length > 0) {
//             if (count <= products.length) {
//                 setLoadMoreDisabled(true);
//             } else {
//                 setLoadMoreDisabled(false);
//             }
//         }
//     }, [count, products.length, page]);

//     return (
//         <>
//             {!loadMoreDisabled && products.length > 0 && (
//                 <Button
//                     callbackHandler={loadMoreHandler}
//                     title={'Load More'}
//                     color={'white'}
//                     disabled={loadMoreDisabled}
//                 />
//             )}
//         </>
//     );
// };
