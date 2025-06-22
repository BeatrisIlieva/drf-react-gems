import type { Review } from '../../../../../types/Products';

export type Params = {
    firstImage: string;
    secondImage: string;
    averageRating: number;
    reviews: Review[];
};
