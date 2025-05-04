import { Component, OnInit } from '@angular/core';
import { Category } from '../types/category';
import { ApiService } from '../api.service';

@Component({
    selector: 'app-nav',
    templateUrl: './nav.component.html',
    styleUrls: ['./nav.component.css'],
})
export class NavComponent implements OnInit {
    categories: Category[] = [];

    constructor(private api: ApiService) {}

    ngOnInit(): void {
        this.api.getCategories().subscribe((data) => {
            this.categories = data;
        });
    }
}
