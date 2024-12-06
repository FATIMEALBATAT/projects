//
//  HomeScreenView.swift
//  LogistikApp
//
//  Created by Fatime Al Batat on 15.10.23.
//

import SwiftUI

struct HomeView: View {
    @EnvironmentObject var vm: AppViewModel
    @State private var isNavigatingToContentView = false
    @State private var isPressed = false

    
    var body: some View {
        NavigationView {
            
            ZStack{
                Color.white
                VStack {
                    Image("homeview")
                        .resizable()
                        .scaledToFit()
                        .frame(width: UIScreen.main.bounds.width, height: 500)
                        .padding(.top, 30)
                    Image("mercedes")
                        .resizable()
                        .scaledToFit()
                        .frame(width: UIScreen.main.bounds.width, height: 70)
                        
                        
                        
                    
                        
                       // .shadow(color: .black, radius: 16, x: 0, y: 5)
                    Text("WAREHOUSE LIZARD")
                        .padding(.bottom, 10)
                        .foregroundColor(.green)
                        .font(.system(size: 24))
                        .frame(alignment: /*@START_MENU_TOKEN@*/.center/*@END_MENU_TOKEN@*/)
                        .bold()
                        
                        .navigationBarTitle("Startseite", displayMode: .inline)
                    NavigationLink(destination: ContentView(), isActive: $isNavigatingToContentView) {
                        
                    }
                    Text("Erfassung von Wareneingängen mit Hilfe von Texterkennung.")
                        .foregroundColor(.black)
                        .font(.system(size: 10))
                        .frame(alignment: /*@START_MENU_TOKEN@*/.center/*@END_MENU_TOKEN@*/)
                    Text("Von Daimler für Daimler.")
                        .foregroundColor(.black)
                        .font(.system(size: 10))
                        .frame(alignment: /*@START_MENU_TOKEN@*/.center/*@END_MENU_TOKEN@*/)
                   
                    
                    HStack {
                        Button(action: {
                                isNavigatingToContentView = true
                            }) {
                                HStack {
                                    Text("Wareneingang erfassen")
                                    Image(systemName: "arrow.right") // Add an arrow icon
                                        .resizable()
                                        .aspectRatio(contentMode: .fit)
                                        .frame(height: 15) // Adjust the size of the arrow
                                }
                            }
                            .padding()
                            .frame(width: 270)
                            .background(Color.green)
                            .foregroundColor(Color.black)
                            .cornerRadius(14)
                        
                        //                    .clipShape(Capsule())
                        //                    .shadow(color: .black, radius: 10, x: 0, y: 5)
                        .scaleEffect(self.isPressed ? 0.9 : 1.0)
                        .padding(.top, 70)
                        .animation(.easeInOut(duration: 0.2), value: self.isPressed) // Fügt eine Animation hinzu
                        .buttonStyle(PlainButtonStyle()) // Entfernt die Standard-Button-Animation
                        .onLongPressGesture(minimumDuration: .infinity, maximumDistance: .infinity, pressing: { isPressing in
                            self.isPressed = isPressing
                        }, perform: {})
                       
                    }
                    
                    Spacer()
                        .frame(height: 40)
                        
                    
           }
 
   }
        } /*.navigationBarHidden(false)*/
    }
}

