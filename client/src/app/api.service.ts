import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment.development';
import { PaginatedProducts } from './types/product';
import { Category } from './types/category';

@Injectable({
    providedIn: 'root',
})
export class ApiService {
    constructor(private http: HttpClient) {}

    getCategories() {
      const { apiUrl } = environment;
      
      return this.http.get<Category[]>(`${apiUrl}/products/categories/`);
    }

    getProducts(page?: number) {
        const { apiUrl } = environment;

        let url = `${apiUrl}/products`;

        if (page) {
            url += `?page=${page}`;
        }

        return this.http.get<PaginatedProducts>(url);
    }
}
