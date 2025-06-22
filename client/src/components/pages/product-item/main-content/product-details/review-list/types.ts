import type { Review } from '../../../../../../types/Products';

export interface Params {
    averageRating: number;
    reviews: Review[];
}
