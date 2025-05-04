import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CoreModule } from './core/core.module';
import { SharedModule } from './shared/shared.module';
import { MainComponent } from './main/main.component';
import { ThemesListComponent } from './themes-list/themes-list.component';
import { ProductsListComponent } from './products-list/products-list.component';
import { HttpClientModule } from '@angular/common/http';
import { NavComponent } from './nav/nav.component';
import { ProductItemComponent } from './products-list/product-item/product-item.component';

@NgModule({
    declarations: [
        AppComponent,
        MainComponent,
        ThemesListComponent,
        ProductsListComponent,
        NavComponent,
        ProductItemComponent,
    ],
    imports: [BrowserModule, AppRoutingModule, CoreModule, SharedModule, HttpClientModule],
    providers: [],
    bootstrap: [AppComponent],
})
export class AppModule {}
