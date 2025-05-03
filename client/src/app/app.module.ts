import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { NavComponent } from './nav/nav.component';
import { NavigationComponent } from './navigation/navigation.component';
import { UserListComponent } from './user-list/user-list.component';
import { PlaygroundComponent } from './playground/playground.component';
import { UserItemComponent } from './user-item/user-item.component';

@NgModule({
    declarations: [
        AppComponent,
        NavComponent,
        NavigationComponent,
        UserListComponent,
        PlaygroundComponent,
        UserItemComponent,
    ],
    imports: [BrowserModule],
    providers: [],
    bootstrap: [AppComponent],
})
export class AppModule {}
