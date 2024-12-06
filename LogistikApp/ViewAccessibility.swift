// View+Accessibility.swift

import SwiftUI

extension View {
    func accessibilityText(_ text: String) -> some View {
        self.accessibilityIdentifier(text)
    }
}
